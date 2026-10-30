from flask import Flask, render_template, request
import re

app = Flask(__name__)


def check_password_strength(password):
    score = 0
    suggestions = []

    # Check password length
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append(
            "Use at least 12 characters for better protection."
        )

    # Check lowercase letters
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append(
            "Add lowercase letters."
        )

    # Check uppercase letters
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append(
            "Add uppercase letters."
        )

    # Check numbers
    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append(
            "Add numbers."
        )

    # Check special characters
    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        suggestions.append(
            "Add special characters such as @, #, or !."
        )

    # Determine strength
    if len(password) < 8:
        strength = "Weak"
    elif score >= 6:
        strength = "Strong"
    elif score >= 4:
        strength = "Medium"
    else:
        strength = "Weak"

    return strength, suggestions


@app.route("/", methods=["GET", "POST"])
def home():
    strength = None
    suggestions = []

    if request.method == "POST":
        password = request.form.get("password", "")

        if password:
            strength, suggestions = check_password_strength(
                password
            )
        else:
            suggestions.append("Please enter a password.")

    return render_template(
        "index.html",
        strength=strength,
        suggestions=suggestions
    )


if __name__ == "__main__":
    app.run(debug=True)