from flask import Flask, request, render_template, session
import os
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session handling

# Predefined Caesar cipher challenge for Station 1
caesar_cipher = {"encoded": "oruhp lsvxp grlorv", "decoded": "lorem ipsum dolor", "hint": "Shift:3 <-"}

# Path to data puzzle images for Station 3
DATA_PUZZLE_FOLDER = "static/images/data_puzzles/"

# Data puzzle mapping for Station 3
data_puzzles = {
    "puzzle1.png": {"answer": "24", "hint": "hint1.png"},
    "puzzle2.png": {"answer": "36", "hint": "hint2.png"},
    "puzzle3.png": {"answer": "7", "hint": "hint3.png"},
    "puzzle4.png": {"answer": "69", "hint": "hint4.png"},
}


@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        manual_code = request.form.get('manual-code', '').strip()
        if manual_code.lower() == "cypher":
            return render_template('/station1.html', challenge=caesar_cipher)
        return render_template('scan.html', feedback="Incorrect code. Try again!")
    return render_template('scan.html')

@app.route('/scan2', methods=['GET', 'POST'])
def scan2():
    if request.method == 'POST':
        manual_code = request.form.get('manual-code', '').strip()
        if manual_code.lower() == "logic":
            return render_template('/station2.html')
        return render_template('scan2.html', feedback="Incorrect code. Try again!")
    return render_template('scan2.html')


@app.route('/scan3', methods=['GET', 'POST'])
def scan3():
    if request.method == 'POST':
        manual_code = request.form.get('manual-code', '').strip()
        if manual_code.lower() == "data":
            # Randomly select a puzzle image
            puzzle_images = list(data_puzzles.keys())
            selected_image = random.choice(puzzle_images)
            session['selected_image'] = selected_image
            
            # Get the corresponding hint image from the dictionary
            hint = data_puzzles[selected_image]["hint"]
            
            # Pass both the puzzle image and hint to the template
            return render_template('station3.html', image=selected_image, hint=hint)

        return render_template('scan3.html', feedback="Incorrect code. Try again!")
    return render_template('scan3.html')


@app.route('/station1', methods=['GET', 'POST'])
def station1():
    if request.method == 'POST':
        answer = request.form.get('decoded-input', '').strip()
        if answer.lower() == caesar_cipher["decoded"]:
            session['station1_answer'] = answer.lower()  # Save answer in session
            feedback = "Correct!"
            return render_template('station1.html', feedback=feedback, challenge=caesar_cipher)
        feedback = "Incorrect answer. Try again!"
        return render_template('station1.html', feedback=feedback, hint=caesar_cipher["hint"], challenge=caesar_cipher)
    return render_template('station1.html', hint=caesar_cipher["hint"], challenge=caesar_cipher)

@app.route('/station2', methods=['GET', 'POST'])
def station2():
    if request.method == 'POST':
        answer = request.form.get('logic-answer', '').strip()
        correct_answer = "7"
        if answer.replace(" ", "").replace(",", "").replace("and", "").strip() == correct_answer.replace(",", "").strip():
            session['station2_answer'] = correct_answer  # Save answer in session
            feedback = "Correct! Proceed to the Next Station"
            return render_template('station2.html', feedback=feedback)
        feedback = "Incorrect answer. Try again!"
        return render_template('station2.html', feedback=feedback)
    return render_template('station2.html')

@app.route('/station3', methods=['GET', 'POST'])
def station3():
    if request.method == 'POST':
        # Get the submitted answer and the selected image
        data_answer = request.form.get('data-answer', '').strip()
        selected_image = session.get('selected_image', '')

        # Check if the submitted answer is correct
        if selected_image in data_puzzles and data_answer == data_puzzles[selected_image]["answer"]:
            session['station3_answer'] = data_answer  # Save answer in session
            return render_template('final.html')  # Redirect to final step on success
        else:
            # If answer is wrong, get the hint image for feedback
            hint = data_puzzles[selected_image]["hint"]
            return render_template(
                'station3.html',
                feedback="Incorrect answer. Try again!",
                image=selected_image,
                hint=hint
            )

    # For GET requests, randomly select an image for the puzzle
    puzzle_images = list(data_puzzles.keys())
    selected_image = random.choice(puzzle_images)
    session['selected_image'] = selected_image  # Save the selected image in session

    # Get the corresponding hint image
    hint = data_puzzles[selected_image]["hint"]

    # Render the station3 page with the selected puzzle and hint
    return render_template(
        'station3.html',
        image=selected_image,
        hint=hint
    )


@app.route('/validate_final_code', methods=['POST'])
def validate_final_code():
    entered_code = request.form.get('final-code', '').strip().lower()

    # Construct the final code dynamically based on session data
    station1_answer = session.get('station1_answer', '').lower()
    station2_answer = session.get('station2_answer', '').lower()
    station3_answer = session.get('station3_answer', '').lower()
    correct_final_code = f"{station1_answer} {station2_answer} {station3_answer}"

    # Normalize user input to remove spaces, commas, and "and"
    normalized_entered_code = entered_code.replace(" ", "").replace(",", "").replace("and", "")

    # Normalize correct final code for comparison
    normalized_correct_code = correct_final_code.replace(" ", "").replace(",", "").replace("and", "")

    if normalized_entered_code == normalized_correct_code:
        return render_template('victory.html')
    else:
        return render_template('final.html', feedback="Incorrect final code. Try again!")

if __name__ == "__main__":
    app.run(debug=True)

