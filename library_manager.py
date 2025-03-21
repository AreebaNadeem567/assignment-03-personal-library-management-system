
import streamlit as st # type: ignore
import pandas as pd # type: ignore
import json
import os
import datetime
import time
import random
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
from streamlit_lottie import st_lottie # type: ignore
import requests  # type: ignore

# set page configuration
st.set_page_config(
    page_title="Personal Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

#custom cs for styling
st.markdown("""
<style>
    .main-header {
       font-size: 3rem !important;
       color: #1E3A8a,
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1)          
    }      
    .su_header{
        font-size: 1.8rem !important;
        color:3B82F6;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 1rem;
     } 
    .success-message {
         padding: 1rem;
         background-color: #ECFDFS;
         border-left: 5px solid #10B981;
         border-radius: 0.375rem;
    }       
    .warning-message {
         padding: 1rem;
         background-color: #FEF3C7;
         border-left: 5px solid #F59E0B;
         border-radius: 0.375rem;  
    }         
    .book-card{
        background-color: #F3F4F6;
        border-radius: 0.5rem;
        padding: Irem;
        narging-bottom: iren;
        border-left: 5px solid #3882F6; I
        transition: transform 6.3s ease; 
    }       
    .book-card-hover{
        transofrm: translateY(-5px);
        box-shadow: 0 10px 15px 3px rgba(0,0,0,0.1);
    }
    .read-badge {
        background-color: #108981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
    }
    .unread-badge {
         background-color: #F87171;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
    }  
    .action-button {
         margin-right: 0.5rem;
            border-radius:0.375rem;   
    }
</style>
""" , unsafe_allow_html=True)

def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None
    
if 'library' not in st.session_state:
    st.session_state.library = []
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'book addded' not in st.session_state:
    st.session_state.book_added = False
if 'book removed' not in st.session_state:
    st.session_state.book_removed = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = "library"

def load_library():
    try:
        if os.path.exists("libray.json"):
            with open("library.json" , "r") as file:
                st.session_state.library = json.load(file)
                return True
            return False
    except Exception as e:
        st.error(f"Error loading library: {e}")
        return False
    
# save Library
def save_library():
    try:
        with open('library.json' , 'w') as file:
            json.dump(st.session_state.library , file)
            return True
    except Exception as e:
         st.error(f"Error loading library: {e}")
         return False
    
# add a book to library
def add_book(title, author, publication_year, genre, read_status):
    book = {
        'title': title,
        'author': author,
        'publication_year': publication_year,
        'genre': genre,
        'read_status': read_status,
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(0.5) #animation delay
    
# remove books
def remove_book(index):
    if 0 <= index < len(st.session_state.library):

        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True
        return True
    return False

#search books
def search_books(search_term, search_by):
    search_term = search_term.lower()
    results = []

    for book in st.session_state.library:
        if search_by == "Title" and search_term in book['title'].lower():
            results.append(book)
        elif search_by == "Author" and search_term in book['author'].lower():
            results.append(book)
        elif search_by == "Genre" and search_term in book['genre'].lower():
            results.append(book)  
        st.session_state.search_results = results 

# calculate library status
def get_library_status():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book ['read status'])
    percent_read = (read_books / total_books * 100) if total_books > 0 else 0

    genres = {}
    authors = {}
    decades = {}

    for book in st.session_state.library:
        if book ['genre'] in genres:
            genres[book['genre']] += 1
        else:
            genres[book['genre']] = 1
            
        #count author
        if book ['author'] in authors:
            authors[book['author']] += 1
        else:
            authors[book['author']] = 1

        #count decade
        decades = (book['publication_year'] // 10) * 10
        if decades in decades:
            decades[decades] += 1
        else:
            decades[decades] = 1

        # sort by count
        genres = dict(sorted(genres.items() , key=lambda x: x[1] , reverse=True))
        authors = dict(sorted(authors.items() , key=lambda x: x[1] , reverse=True))
        decades = dict(sorted(decades.items() , key=lambda x: x[0]))

        return {
            'total_books': total_books,
            'read_books': read_books,
            'percent_read': percent_read,
            'genres': genres,
            'authors': authors,
            'decades': decades
        }

        


def create_visualizations(stats):
    if stats['total_books'] > 0:
        fig_read_status = go.Figure(data=[go.Pie(
            labels=['Read', 'Unread'],
            values=[stats['read_books'], stats['total_books'] - stats['read_books']],
            hole=.4,
            marker=dict(colors=['#10B981', '#F87171'])
        )])
        fig_read_status.update_layout(
            title_text="Read vs Unread Books",
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig_read_status, use_container_width=True)

    # Bar chart for genres
    if stats['geners']:
        geners_df = pd.DataFrame({
            'Geners': list(stats['geners'].keys()),
            'Count': list(stats['geners'].values())
        })
        fig_geners = px.bar(
            geners_df,
            x='Geners',
            y='Count',
            color='Count',
            color_continuous_scale=px.colors.sequential.Blues
        )
        fig_geners.update_layout(
            title_text='Books by Genre',
            xaxis_title='Genre',
            yaxis_title='Number of Books',
            height=400
        )
        st.plotly_chart(fig_geners, use_container_width=True)

    # Line chart for decades
    if stats['decades']:
        decades_df = pd.DataFrame({
            'Decade': [f"{decade}s" for decade in stats['decades'].keys()],
            'Count': list(stats['decades'].values()),
        })
        fig_decades = px.line(
            decades_df,
            x='Decade',
            y='Count',
            line_shape="spline"
        )
        fig_decades.update_layout(
            title_text='Books by Publication Decade',
            xaxis_title='Decade',
            yaxis_title='Number of Books',
            height=400
        )
        st.plotly_chart(fig_decades, use_container_width=True)

# Load external assets (fix unsafe_allow_html=True issue)
st.sidebar.markdown("<h1 style='text-align: center;'>Library Statistics</h1>", unsafe_allow_html=True)

def load_lottieurl(url):
    return url  # Dummy function to prevent errors (replace with actual loading function)

lottie_book = load_lottieurl("https://assets9.lottiefiles.com/temp/1f20_aKAfIn.json")
if lottie_book:
    with st.sidebar:
        st.lottie(lottie_book, height=200, key='book_animation')

# Navigation options
nav_options = st.sidebar.radio(
    "Choose an option:",
    ["View Library", "Add Book", "Search Books", "Library Statistics"]
)

if nav_options == "View Library":
    st.session_state.current_view = "library"
elif nav_options == "Add Book":
    st.session_state.current_view = "add"
elif nav_options == "Search Books":
    st.session_state.current_view = "search"
elif nav_options == "Library Statistics":
    st.session_state.current_view = "stats"



st.markdown("<h1 class='main-header'> 📚 Personal Library Manager </h1>", unsafe_allow_html=True)

if "current_view" not in st.session_state:
    st.session_state.current_view = "library"
if "book_added" not in st.session_state:
    st.session_state.book_added = False
if "book_removed" not in st.session_state:
    st.session_state.book_removed = False
if "library" not in st.session_state:
    st.session_state.library = []

if st.session_state.current_view == "add":
    st.markdown("<h2 class='sub-header'> ➕ Add a Book </h2>", unsafe_allow_html=True)

    # Adding books input form
    with st.form(key='add_book_form'):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("📖 Book Title", max_chars=100)
            author = st.text_input("✍️ Author", max_chars=100)
            publication_year = st.number_input("📅 Publication Year", min_value=1000, max_value=datetime.now().year, step=1, value=2023)

        with col2:
            genre = st.selectbox("📂 Genre", [
                "Fiction",
                "Non-Fiction",
                "Science",
                "Technology",
                "Fantasy",
                "Romance",
                "Poetry",
                "Self-help",
                "Art",
                "Religion",
                "History",
                "Other"
            ])
            read_status = st.radio("📖 Read Status", ["✅ Read", "📌 Unread"], horizontal=True)
            read_bool = read_status == "✅ Read"
            submit_button = st.form_submit_button("📥 Add Book")

        if submit_button and title and author:
            st.session_state.library.append({
                "title": title,
                "author": author,
                "publication_year": publication_year,
                "genre": genre,
                "read_status": read_bool
            })
            st.session_state.book_added = True

    if st.session_state.book_added:
        st.markdown("<div class='success-message'> ✅ Book added successfully! 📚</div>", unsafe_allow_html=True)
        st.balloons()
        st.session_state.book_added = False

elif st.session_state.current_view == "library":
    st.markdown("<h2 class='sub-header'> 📚 Your Library </h2>", unsafe_allow_html=True)

    if not st.session_state.library:
        st.markdown("<div class='warning-message'> ⚠️ Your library is empty! Add some books to get started! </div>", unsafe_allow_html=True)
    else:
        cols = st.columns(2)
        for i, book in enumerate(st.session_state.library):
            with cols[i % 2]:
                st.markdown(f"""
                <div class='book-card'>
                    <h3>📖 {book['title']}</h3>
                    <p><strong>✍️ Author:</strong> {book['author']}</p>
                    <p><strong>📅 Publication Year:</strong> {book['publication_year']}</p>
                    <p><strong>📂 Genre:</strong> {book['genre']}</p>
                    <p><span class={'read-badge' if book['read_status'] else 'unread-badge'}>
                        {"✅ Read" if book['read_status'] else "📌 Unread"}
                    </span></p>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Remove", key=f"remove-{i}", use_container_width=True):
                        del st.session_state.library[i]
                        st.session_state.book_removed = True
                        st.rerun()
                with col2:
                    new_status = not book['read_status']
                    status_label = "📖 Mark as Read" if not book["read_status"] else "📌 Mark as Unread"
                    if st.button(status_label, key=f"status-{i}", use_container_width=True):
                        st.session_state.library[i]['read_status'] = new_status
                        st.rerun()

if st.session_state.book_removed:
    st.markdown("<div class='success-message'> 🗑️ Book removed successfully! </div>", unsafe_allow_html=True)
    st.session_state.book_removed = False

elif st.session_state.current_view == "search":
    st.markdown("<h2 class='sub-header'> 🔍 Search Books </h2>", unsafe_allow_html=True)



# .............................

    search_by = st.selctbox("Search by:", ["Title", "Author", "Genre"])
    search_term = st.text_input("Enter search term:")

    if st.button("Search", use_container_width=False):
       if search_term:
         with st.spinner("Searching..."):
           time.sleep(0.5)
           search_books(search_term, search_by)
    if hasattr(st.session_state, 'search_results'):
        if st.session_state.search_results:
           st.markdown(f"<h3>Found {len(st.session_state.search_results)} results:</h3>", unsafe_allow_html=True)
        
        for i, book in enumerate(st.session_state.search_results):
            st.markdown(f"""
                       <div class = 'book-card>
                       <h3>{book['title']}</h3
                       <p><strong>Author:</strong> {book['author']}</p>
                       <p><strong>Publication Year:</strong> {book['publication_year']}</p>
                       <p><strong>Genre:</strong> {book['genre']}</p>
                       <p><span class="{'read-badge' if book['read_status'] else 'unread-badge'}">{
                       'Read' if book['read_status'] else 'Unread'
                       }</span></p>
                      </div>
""", unsafe_allow_html=True)
    elif search_term:
          st.markdown("<div class= 'warning-message'> No books found matching your search.</div>, unsafe_allow_html=True")    

elif st.session_state.current_view == "stats":
    st.markdown("<h2 class='sub-header'>Library Statistics</h2>", unsafe_allow_html=True)

    if not st.session_state.library:
        st.markdown("<div class='warning-message'>Your library is empty. Add some books to see stats!</div>", unsafe_allow_html=True)
    else:
        stats = get_library_status()  # Assuming this function is defined elsewhere
        col1,col2,col3 = st.columns(3)
        with col1:
            st.metric("Total Books", stats['total_books'])
        with col2:
            st.metric("Books Read", stats['read_books'])
        with col3:
            st.metric("Percentage Read", f"{stats['percentage_read'] :.1f}%")
        create_visualizations()

        if stats['authors']:
          st.markdown("<h3>Top Authors</h3>", unsafe_allow_html=True)
          top_authors = dict(list(stats['authors'].items())[:5])
          for author, count in top_authors.items():
           st.markdown(f"**{author}**: {count} book{'s' if count > 1 else ''}")
st.markdown("---")
st.markdown("Copyright © 2025 Areeba Nadeem Personal Library Manager", unsafe_allow_html=True)
