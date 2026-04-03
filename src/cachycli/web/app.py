"""Flask web application for CachyCLI."""

from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from cachycli.core.lesson_loader import load_all_lessons, load_lesson
from cachycli.core.progress import ProgressDB
from cachycli.core.quiz_engine import check_answer, load_lesson_quiz, load_weekly_quiz
from cachycli.core.scheduler import (
    TOTAL_LESSONS,
    current_week,
    is_week_complete,
    next_lesson_id,
    week_progress,
)
from cachycli.utils.config import get_api_key, save_api_key
from cachycli.utils.sandbox import Sandbox

_WEEK_NAMES = [
    "Terminal & Navigation",
    "File Operations",
    "Viewing & Editing",
    "Permissions & Users",
    "Text Processing",
    "Pipes & Redirection",
    "System Admin (CachyOS)",
]


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(Path(__file__).parent / "templates"),
        static_folder=str(Path(__file__).parent / "static"),
    )
    app.secret_key = "cachycli-local-only"

    # Keep a sandbox per session (simple single-user model).
    _sandboxes: dict[str, Sandbox] = {}

    def _db() -> ProgressDB:
        return ProgressDB()

    # -- Pages -----------------------------------------------------------------

    @app.route("/")
    def index():
        return render_template("index.html")

    # -- API: Lessons ----------------------------------------------------------

    @app.route("/api/lessons")
    def api_lessons():
        db = _db()
        try:
            lessons = load_all_lessons()
            completed = set(db.completed_lesson_ids())
            result = []
            for les in lessons:
                result.append(
                    {
                        "id": les.id,
                        "week": les.week,
                        "title": les.title,
                        "completed": les.id in completed,
                        "duration": les.duration_minutes,
                        "objectives": les.objectives,
                        "commands": les.commands,
                    }
                )
            return jsonify(result)
        finally:
            db.close()

    @app.route("/api/lesson/<int:lesson_id>")
    def api_lesson(lesson_id: int):
        db = _db()
        try:
            les = load_lesson(lesson_id)
            return jsonify(
                {
                    "id": les.id,
                    "week": les.week,
                    "title": les.title,
                    "duration": les.duration_minutes,
                    "objectives": les.objectives,
                    "commands": les.commands,
                    "body": les.body,
                    "completed": db.is_lesson_completed(lesson_id),
                    "sandbox_commands": les.sandbox_commands,
                    "sandbox_setup": les.sandbox_setup,
                }
            )
        except FileNotFoundError:
            return jsonify({"error": "Lesson not found"}), 404
        finally:
            db.close()

    @app.route("/api/lesson/<int:lesson_id>/complete", methods=["POST"])
    def api_complete_lesson(lesson_id: int):
        db = _db()
        try:
            db.complete_lesson(lesson_id)
            return jsonify({"ok": True})
        finally:
            db.close()

    # -- API: Quizzes ----------------------------------------------------------

    @app.route("/api/quiz/lesson/<int:lesson_id>")
    def api_lesson_quiz(lesson_id: int):
        try:
            quiz = load_lesson_quiz(lesson_id)
            questions = []
            for q in quiz.questions:
                questions.append(
                    {
                        "type": q.type,
                        "question": q.question,
                        "choices": q.choices,
                    }
                )
            return jsonify(
                {
                    "quiz_type": quiz.quiz_type,
                    "quiz_id": quiz.quiz_id,
                    "questions": questions,
                }
            )
        except FileNotFoundError:
            return jsonify({"error": "Quiz not found"}), 404

    @app.route("/api/quiz/weekly/<int:week>")
    def api_weekly_quiz(week: int):
        try:
            quiz = load_weekly_quiz(week)
            questions = []
            for q in quiz.questions:
                questions.append(
                    {
                        "type": q.type,
                        "question": q.question,
                        "choices": q.choices,
                    }
                )
            return jsonify(
                {
                    "quiz_type": quiz.quiz_type,
                    "quiz_id": quiz.quiz_id,
                    "questions": questions,
                }
            )
        except FileNotFoundError:
            return jsonify({"error": "Quiz not found"}), 404

    @app.route("/api/quiz/submit", methods=["POST"])
    def api_submit_quiz():
        data = request.get_json()
        quiz_type = data.get("quiz_type", "lesson")
        quiz_id = data.get("quiz_id", "")
        answers = data.get("answers", [])

        # Load the quiz to check answers.
        if quiz_type == "weekly":
            week = int(quiz_id.split("_")[1])
            quiz = load_weekly_quiz(week)
        else:
            lid = int(quiz_id.split("_")[1])
            quiz = load_lesson_quiz(lid)

        results = []
        score = 0
        for i, q in enumerate(quiz.questions):
            user_ans = answers[i] if i < len(answers) else ""
            correct = check_answer(q, str(user_ans))
            if correct:
                score += 1

            if q.type == "multiple_choice":
                correct_display = q.choices[q.answer] if isinstance(q.answer, int) else str(q.answer)
            elif q.type == "true_false":
                correct_display = "True" if q.answer else "False"
            else:
                correct_display = str(q.answer)

            results.append(
                {
                    "correct": correct,
                    "correct_answer": correct_display,
                    "explanation": q.explanation,
                }
            )

        total = len(quiz.questions)
        pct = (score / total * 100) if total else 0

        db = _db()
        try:
            db.record_quiz(quiz_type, quiz_id, score, total)
        finally:
            db.close()

        return jsonify(
            {
                "score": score,
                "total": total,
                "percentage": round(pct, 1),
                "passed": pct >= 70,
                "results": results,
            }
        )

    # -- API: Progress ---------------------------------------------------------

    @app.route("/api/progress")
    def api_progress():
        db = _db()
        try:
            current_streak, longest_streak = db.get_streak()
            completed_count = db.completed_count()
            quiz_results = db.all_quiz_results()

            avg_score = 0.0
            if quiz_results:
                avg_score = sum(r.percentage for r in quiz_results) / len(quiz_results)

            weeks = []
            for w in range(1, 8):
                done, total = week_progress(db, w)
                best = db.best_quiz_result("weekly", f"week_{w:02d}")
                weeks.append(
                    {
                        "week": w,
                        "name": _WEEK_NAMES[w - 1],
                        "done": done,
                        "total": total,
                        "quiz_score": best.percentage if best else None,
                        "quiz_passed": best.percentage >= 70 if best else False,
                    }
                )

            nxt = next_lesson_id(db)

            return jsonify(
                {
                    "current_streak": current_streak,
                    "longest_streak": longest_streak,
                    "completed": completed_count,
                    "total_lessons": TOTAL_LESSONS,
                    "avg_score": round(avg_score, 1),
                    "weeks": weeks,
                    "next_lesson": nxt,
                }
            )
        finally:
            db.close()

    @app.route("/api/progress/reset", methods=["POST"])
    def api_reset():
        db = _db()
        try:
            db.reset()
            return jsonify({"ok": True})
        finally:
            db.close()

    # -- API: Sandbox ----------------------------------------------------------

    @app.route("/api/sandbox/start", methods=["POST"])
    def api_sandbox_start():
        data = request.get_json() or {}
        allowed = data.get("allowed_commands")
        setup = data.get("setup_script", "")

        # Clean up any existing sandbox.
        if "default" in _sandboxes:
            try:
                _sandboxes["default"].__exit__(None, None, None)
            except Exception:
                pass

        sb = Sandbox(allowed_commands=allowed, setup_script=setup)
        sb.__enter__()
        _sandboxes["default"] = sb
        return jsonify({"ok": True, "path": sb.path})

    @app.route("/api/sandbox/run", methods=["POST"])
    def api_sandbox_run():
        data = request.get_json()
        command = data.get("command", "")
        sb = _sandboxes.get("default")
        if not sb:
            return jsonify({"error": "No sandbox active. Start one first."}), 400
        result = sb.run(command)
        return jsonify(
            {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "timed_out": result.timed_out,
            }
        )

    @app.route("/api/sandbox/stop", methods=["POST"])
    def api_sandbox_stop():
        sb = _sandboxes.pop("default", None)
        if sb:
            try:
                sb.__exit__(None, None, None)
            except Exception:
                pass
        return jsonify({"ok": True})

    # -- API: Settings ---------------------------------------------------------

    @app.route("/api/settings", methods=["GET"])
    def api_get_settings():
        key = get_api_key()
        # Only reveal whether a key is set, never the full key.
        return jsonify({"has_api_key": bool(key), "api_key_preview": key[:8] + "..." if len(key) > 8 else ""})

    @app.route("/api/settings", methods=["POST"])
    def api_save_settings():
        data = request.get_json() or {}
        key = data.get("api_key", "").strip()
        if not key:
            return jsonify({"error": "API key is required."}), 400
        save_api_key(key)
        return jsonify({"ok": True})

    # -- API: Chat (Claude AI assistant) ------------------------------------

    @app.route("/api/chat", methods=["POST"])
    def api_chat():
        data = request.get_json() or {}
        user_message = data.get("message", "").strip()
        lesson_id = data.get("lesson_id")
        chat_history = data.get("history", [])

        if not user_message:
            return jsonify({"error": "Message is required."}), 400

        key = get_api_key()
        if not key:
            return jsonify({"error": "no_api_key"}), 400

        # Build context from current lesson.
        lesson_context = ""
        if lesson_id:
            try:
                les = load_lesson(lesson_id)
                lesson_context = (
                    f"The student is currently on Lesson {les.id} (Week {les.week}): "
                    f'"{les.title}".\n'
                    f"Learning objectives: {', '.join(les.objectives)}\n"
                    f"Key commands: {', '.join(les.commands)}\n\n"
                    f"--- Lesson Content ---\n{les.body}\n--- End Lesson Content ---"
                )
            except FileNotFoundError:
                pass

        system_prompt = (
            "You are CachyCLI Tutor, a friendly and knowledgeable Linux teaching assistant "
            "embedded in the CachyCLI learning app. The student is learning Linux command-line "
            "skills through a structured 7-week, 35-lesson curriculum on CachyOS (Arch-based).\n\n"
            "Guidelines:\n"
            "- Answer questions about the current lesson, Linux commands, and related concepts.\n"
            "- Give practical examples using real commands they can try in the practice terminal.\n"
            "- Keep answers concise but thorough — aim for 2-4 short paragraphs max.\n"
            "- Use markdown formatting (backticks for commands, code blocks for examples).\n"
            "- If the student asks about topics from future lessons, give a brief answer "
            "but mention which lesson covers it in depth.\n"
            "- Be encouraging and patient — they are learning.\n"
            "- Reference CachyOS/Arch specifics when relevant (pacman, paru, systemd, etc.).\n"
        )

        if lesson_context:
            system_prompt += f"\n{lesson_context}"

        try:
            import anthropic

            client = anthropic.Anthropic(api_key=key)

            # Build messages from chat history + new message.
            messages = []
            for msg in chat_history[-20:]:  # Keep last 20 messages for context.
                messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": user_message})

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=system_prompt,
                messages=messages,
            )

            reply = response.content[0].text
            return jsonify({"reply": reply})

        except anthropic.AuthenticationError:
            return jsonify({"error": "Invalid API key. Please update it in Settings."}), 401
        except anthropic.RateLimitError:
            return jsonify({"error": "Rate limited. Please wait a moment and try again."}), 429
        except Exception as e:
            return jsonify({"error": f"Chat error: {str(e)}"}), 500

    return app


def run_web(host: str = "127.0.0.1", port: int = 8080) -> None:
    app = create_app()
    print(f"\n  CachyCLI Web UI: http://{host}:{port}\n")
    app.run(host=host, port=port, debug=False)
