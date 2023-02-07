import pickle
from flask import Flask,render_template,request,url_for
import numpy as np
import pandas as pd

popular_books = pickle.load(open('popular_books.pkl','rb'))
pivot = pickle.load(open('pivot.pkl','rb'))
books = pickle.load(open('books_list.pkl','rb'))
similarity = pickle.load(open('similarity_scores.pkl','rb'))

app=Flask(__name__)

@app.route('/')
def pop_books():
    return render_template('index.html',
                           len=len(popular_books),
                           book_title=list(popular_books['Book-Title'].values),
                           book_author=list(popular_books['Book-Author'].values),
                           image=list(popular_books['Image-URL-M'].values),
                           votes=list(popular_books['num_rating'].values),
                           avg_rating=np.round(list(popular_books['avg_rating'].values),2)
                           )

@app.route('/recomm')
def recommend_ui():
    return render_template('recomm.html')

@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input_book=request.form.get('user_input')
    index=np.where(pivot.index==user_input_book)[0][0]
    recommended_books=sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    data=[]
    for i in recommended_books[1:6]:
        lists=[]
        book_name_df=books[books['Book-Title']==pivot.index[i[0]]]
        #lists.extend(books[books['Book-Title']==book_name])
        lists.extend(book_name_df.drop_duplicates('Book-Title')['Book-Title'].values)
        lists.extend(book_name_df.drop_duplicates('Book-Title')['Book-Author'].values)
        lists.extend(book_name_df.drop_duplicates('Book-Title')['Image-URL-M'].values)
        data.append(lists)
    print(data)
    return render_template('recomm.html',data=data)


if __name__=='__main__':
    app.run(debug=True)


    
