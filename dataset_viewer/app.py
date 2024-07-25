# simple test changes
from flask import Flask, render_template, request, jsonify, session
import pandas as pd
from datasets import Dataset
import yaml
import jinja2
import os
from collections import OrderedDict
from bs4 import BeautifulSoup
from compiler_fuzzing import cfg_reader

app = Flask(__name__)
app.secret_key = 'fuzzing' 

# Assuming the dataset is in CSV format
# dataset = Dataset.from_csv('../data/generated_yaml/20230513-233833/manifest_ds.csv')

# df = pd.read_csv('../data/generated_yaml/20230513-233833/manifest_ds.csv')
timestamp = '20230605-102821'

input_file = f'../data/generated_yaml/{timestamp}/manifest_ds.csv'
output_file = f'annotations/{timestamp}.csv'

# Check if the output file exists
if not os.path.exists(output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # List of new column names and their corresponding values
    new_columns = {'relevance': 0, 'generate_bug': 0, 'comment': ''}

    # Create new columns if they don't exist
    for column_name, column_value in new_columns.items():
        if column_name not in df.columns:
            df[column_name] = column_value

    # Save the updated DataFrame to the output CSV file
    df.to_csv(output_file, index=False)
else:
    print("Output file already exists.")
# Create a list of all unique ids
df = Dataset.from_csv(output_file)
# breakpoint()
ids = list(OrderedDict.fromkeys(df['id']))

# Initialize an index to keep track of the current id
current_id_index = 0

def clean_html_tags(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    cleaned_text = soup.get_text(separator=' ')
    return cleaned_text

def format_output(output):
    """Format Ansible output with HTML tags for color coding."""
    if isinstance(output, str):
        output = output.replace("[command]", '<span class="command">[command]</span>')
        output = output.replace("[SUCCESS]", '<span class="success">[SUCCESS]</span>')
        output = output.replace("[ERROR]", '<span class="error">[ERROR]</span>')
    return output

@app.route('/', methods=['GET', 'POST'])
def home():
    global current_id_index
    # Fetch all rows with the current id
    
    # breakpoint()
    df = Dataset.from_csv(output_file)
    cfg = cfg_reader.primary.load("../confs/config.yaml")
    level_list =  [int(x) for x in cfg['levels'].split(",")]
    
    if request.method == 'POST':
        # Get filter parameters from form
        
        if 'next' in request.form:
            current_id_index += 1
            syntax = session.get('syntax', [])
            level = session.get('level', [])
        elif 'previous' in request.form:
            syntax = session.get('syntax', [])
            level = session.get('level', [])
            current_id_index -= 1
            if current_id_index < 0: 
                current_id_index += 1
        else:
            syntax = request.form.getlist('syntax')
            level = request.form.getlist('level')
            # Store filter parameters in session
            
            syntax = [int(x) for x in syntax]
            level = [int(x) for x in level]
            
            session['syntax'] = syntax
            session['level'] = level
    else:
        # Get filter parameters from session
        syntax = session.get('syntax', [])
        level = session.get('level', [])

    # Get filter parameters
    # syntax = session.get('syntax', request.form.getlist('syntax'))
    # level = session.get('level', request.form.getlist('level'))
    rows = df.filter(lambda example: example['id'] ==ids[current_id_index])
    # breakpoint()
    # Filter data
    if syntax:
        rows = [row for row in rows if row['syntax'] in syntax]
    if level:
        rows = [row for row in rows if row['level'] in level]

    
    for row in rows:
        if 'output' in row:
            row['output'] = format_output(row['output'])
        # if 'comment' in row:
        #     row['comment'] = clean_html_tags(row['comment'])
        for key, value in row.items():
            if isinstance(value, str) and key in ['sys_role', 'prompt', 'response']:
                row[key] = value.replace('\n', '<br>').replace('\\n', '<br>')
    # breakpoint()
    return render_template('index.html', rows=rows, syntax=syntax, level=level, level_list=level_list)

@app.route('/save', methods=['POST'])
def save_annotations():
    global current_id_index
    # Get annotations from request
    annotations = request.json
    
    # Save annotations to a file
    with open('annotations/log.txt', 'a') as f:
        for annotation in annotations:
            f.write(str(annotation) + '\n')
    # Increment the index to get the next id
    def update_func(sample):
        for annotation in annotations:
            relevance = int(annotation['relevance'])
            generate_bug = int(annotation['generate_bug'])
            sample_id = int(annotation['id'])
            level = int(annotation['level'])
            comment = annotation['comment']
            if sample['id'] == sample_id and sample['level'] == level:
                
                sample.update({
                    'relevance' : relevance,
                    'generate_bug' : generate_bug,
                    'comment' : comment
                })
        return sample
    df = Dataset.from_csv(output_file)
    output_ds = df.map(update_func)
    # row = df[(df['id'] == int(annotation['id'])) & (df['level'] == int(annotation['level']))]
    output_ds.to_csv(output_file)
    
    # df = output_ds
    
    
    # current_id_index += 1
    # # Fetch the rows for the next id and return them
    # next_rows = df.filter(lambda example: example['id'] == ids[current_id_index])
    # df[df['id'] == ids[current_id_index]].to_dict(orient='records')
    # breakpoint()
    return "Success"

def load_and_filter_dataset(request):
    # Load the dataset (replace this with your own dataset loading logic)
    dataset = Dataset.from_csv(output_file)
    # breakpoint()
    if request.method == 'POST':
        # Save filters to session
        session['syntax_view'] = request.form.get('syntax')
        session['relevance_view'] = request.form.get('relevance')
        session['level_view'] = request.form.getlist('level')
        session['generate_bug_view'] = request.form.get('generate_bug')

        # Rest of your view function...

    # Get filters from session
    syntax = session.get('syntax_view')
    relevance = session.get('relevance_view')
    level = session.get('level_view')
    generate_bug = session.get('generate_bug_view')

    # Apply filters to the dataset
    filtered_dataset = dataset
    
    # breakpoint()
    
    level = [] if level is None else [int(x) for x in level]

    # Apply filters
    if syntax:
        filtered_dataset = filtered_dataset.filter(lambda x: x['syntax'] == int(syntax))
    if relevance:
        filtered_dataset = filtered_dataset.filter(lambda x: x['relevance'] == int(relevance))
    if level:
        filtered_dataset = filtered_dataset.filter(lambda x: x['level'] in level)
    if generate_bug:
        filtered_dataset = filtered_dataset.filter(lambda x: x['generate_bug'] == int(generate_bug))

    return filtered_dataset, syntax, relevance, level, generate_bug


def paginate_dataset(dataset, page_number, limit):
    start_index = (page_number - 1) * limit
    end_index = start_index + limit
    paginated_dataset = dataset[start_index:end_index]
    paginated_hf_dataset = Dataset.from_dict(paginated_dataset)
    return paginated_hf_dataset, end_index



@app.route('/view', methods=['GET', 'POST'])
def view():
    page = request.args.get('page', 1, type=int)
    
    cfg = cfg_reader.primary.load("../confs/config.yaml")
    level_list =  [int(x) for x in cfg['levels'].split(",")]
    filtered_dataset, syntax, relevance, level, generate_bug = load_and_filter_dataset(request)

    length = len(filtered_dataset)
    # Apply pagination
    page_items, end = paginate_dataset(filtered_dataset, page, 10)
    # start = (page - 1) * 10
    # end = start + 10
    # page_items = filtered_dataset[start:end]
    
    # level = []
    # breakpoint()
    return render_template(
        'view.html', 
        page_items = page_items, 
        page = page, 
        has_next = end < len(filtered_dataset),
        syntax = syntax, 
        relevance = relevance, 
        level = level, 
        generate_bug = generate_bug,
        length = length,
        level_list = level_list
        )


@app.template_filter('yaml')
def yaml_filter(data):
    diction = data
    try:
        
        diction = yaml.safe_load(data)
    except:
        yaml.dump(diction)
    return yaml.dump(diction)

if __name__ == '__main__':
    app.run(debug=True)
