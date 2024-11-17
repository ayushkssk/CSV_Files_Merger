from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if files are uploaded
        if 'file1' not in request.files or 'file2' not in request.files:
            return "Please upload both files", 400

        file1 = request.files['file1']
        file2 = request.files['file2']

        # Read the uploaded CSV files
        data1 = pd.read_csv(file1)
        data2 = pd.read_csv(file2)

        # Merge the datasets on 'Name' and "Father's Name"
        merged_data = pd.merge(
            data1, 
            data2, 
            left_on=['candidate_name', 'father_name'], 
            right_on=['Name', 'Fathers Name'], 
            how='inner'
        )

        # Extract the 'Student ID' from the merged data
        student_ids = merged_data[['candidate_name', 'father_name', 'Stu ID']]

        # Save the result to a new Excel file
        output_filename = 'merged_student_ids.xlsx'
        student_ids.to_excel(output_filename, index=False)

        # Send the file to the user
        return send_file(output_filename, as_attachment=True)

    return render_template('index.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

if __name__ == '__main__':
    app.run(debug=True)
