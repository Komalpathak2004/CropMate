from flask import Flask, render_template, request
import cv2
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def calculate_area(image_path):
    if not image_path:
        return 0
    image = cv2.imread(image_path)
    if image is None:
        return 0
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total_area = sum(cv2.contourArea(contour) for contour in contours)
    return total_area

def calculate_seed_amount(area, seed_density):
    seed_amount = area * seed_density
    return seed_amount

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error_message = None
    if request.method == 'POST':
        seed_density = request.form.get('density')
        file = request.files.get('image')

        if file and seed_density:
            # Check for valid file type
            if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                error_message = "Invalid file type. Please upload a valid image."
            else:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(image_path)

                land_area = calculate_area(image_path)
                if land_area <= 0:
                    error_message = "Could not calculate the area from the uploaded image."
                else:
                    seed_density = int(seed_density)
                    seed_amount = calculate_seed_amount(land_area, seed_density)
                    result = f"Total area of the land: {land_area:.2f} square meters<br>Approximate amount of seeds/plants needed: {seed_amount:.2f} seeds/plants"

                # Optionally remove the uploaded image after processing
                os.remove(image_path)
        else:
            error_message = "Please provide both seed density and image."

    return render_template('home.html', result=result, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
