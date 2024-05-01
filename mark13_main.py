#import libraries
import json
from flask import Flask, jsonify, request

#import user-defined modules
import mark13_df

app = Flask(__name__)

# Define the base URL for Flipkart search
base_url = "https://www.flipkart.com/search?q="

# API endpoint to scrape Flipkart based on search word
@app.route('/scrape_flipkart', methods=['GET'])
def scrape_flipkart():
    search_word = request.args.get('search_word')
    if not search_word:
        return jsonify({'Enter a Search Word':''})

    url = base_url + search_word
    df = mark13_df.get_df(url, search_word)
    print(df)

    # Convert DataFrame to JSON and return
    json_data = df.to_json(orient='records')
    return json_data

if __name__ == '__main__':
    app.run(debug=True)


#http://127.0.0.1:5000/scrape_flipkart?search_word=
