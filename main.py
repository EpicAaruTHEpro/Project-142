from flask import Flask, json, jsonify, request
from flask_cors import CORS
from storage import all_articles, liked_articles, not_liked_articles
from demographic_filtering import output
from content_filtering import get_recomendations

app =Flask(__name__)
CORS(app)

@app.route('/get-article')
def get_article():
    article_data = {
        'title': all_articles[0][12],
        'interactions': all_articles[0][15],
        'text': all_articles[0][13]
    }
    return jsonify({
        'data': article_data,
        'status': "success"
    })

@app.route('/liked-article', methods=['POST'])
def liked_article():
    global all_articles
    article = all_articles[0]
    all_articles = all_articles[1:]
    liked_articles.append(article)
    return jsonify({
        'status': "success"
    })

@app.route('/not-liked-article', methods=['POST'])
def not_liked_article():
    global all_articles
    article = all_articles[0]
    all_articles = all_articles[1:]
    not_liked_articles.append(article)
    return jsonify({
        'status': 'success'
    })

@app.route('/popular-articles')
def popular_articles():
    article_data = []
    for article in output:
        data2 = {
            'title': article[0],
            'interactions': article[1],
            'text': article[2]
        }
        article_data.append(data2)
    
    return jsonify({
        'data': article_data,
        'status' : 'success'
    })

@app.route('/recommended-articles')
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recomendations(liked_article[12])
        for data in output:
            all_recommended.append(data)
    
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended, _ in itertools.groupby(all_recommended))

    article_data = []
    for article in all_recommended:
        data2 = {
            'title': article[0],
            'interactions': article[1],
            'text': article[2]
        }
        article_data.append(data2)
    
    return jsonify({
        'data': article_data,
        'status' : 'success'
    })

if (__name__ == "__main__"):
    app.run(debug=True)
