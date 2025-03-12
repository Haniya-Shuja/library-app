import streamlit as st
import json

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        color: #2e7d32;
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        border-bottom: 2px solid #2e7d32;
        margin-bottom: 30px;
    }
    .subheader {
        color: #1565c0;
        font-size: 2em;
        padding: 10px 0;
    }
    .book-card {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #2e7d32;
    }
    .success-msg {
        color: #2e7d32;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-msg {
        color: #f57c00;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .sidebar-content {
        padding: 20px;
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

def load_library():
    try:
        with open('library.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_library(library):
    with open('library.json', 'w') as file:
        json.dump(library, file, indent=4)

def add_book():
    st.markdown('<p class="subheader">📚 Add New Book</p>', unsafe_allow_html=True)
    title = st.text_input('📖 Title')
    author = st.text_input('✍️ Author')
    rating = st.number_input('⭐ Rating', 
                           min_value=0.0,
                           max_value=5.0,
                           step=0.5,
                           value=0.0)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button('Add Book 📚', use_container_width=True):
            library.append({'title': title, 'author': author, 'rating': float(rating)})
            save_library(library)
            st.markdown('<p class="success-msg">✅ Book added successfully!</p>', unsafe_allow_html=True)

def view_books():
    st.markdown('<p class="subheader">📚 Your Book Collection</p>', unsafe_allow_html=True)
    if not library:
        st.markdown('<p class="warning-msg">📭 Your library is empty!</p>', unsafe_allow_html=True)
    for book in library:
        st.markdown(f"""
        <div class="book-card">
            📖 <b>Title:</b> {book['title']}<br>
            ✍️ <b>Author:</b> {book['author']}<br>
            ⭐ <b>Rating:</b> {book['rating']}
        </div>
        """, unsafe_allow_html=True)

def edit_book():
    st.markdown('<p class="subheader">✏️ Edit Book</p>', unsafe_allow_html=True)
    if library:
        book_titles = [book['title'] for book in library]
        selected_title = st.selectbox('📚 Select a book to edit', book_titles)
        
        selected_book = next((book for book in library if book['title'] == selected_title), None)
        
        if selected_book:
            edited_book = {}
            edited_book['title'] = st.text_input('📖 Title', value=selected_book['title'])
            edited_book['author'] = st.text_input('✍️ Author', value=selected_book['author'])
            edited_book['rating'] = st.number_input('⭐ Rating', 
                                                  min_value=0.0,
                                                  max_value=5.0,
                                                  step=0.5,
                                                  value=float(selected_book['rating']))

            col1, col2, col3 = st.columns([1,1,1])
            with col2:
                if st.button('Update Book ✨', use_container_width=True):
                    for i, book in enumerate(library):
                        if book['title'] == selected_title:
                            library[i] = edited_book
                            save_library(library)
                            st.markdown('<p class="success-msg">✅ Book updated successfully!</p>', 
                                      unsafe_allow_html=True)
                            break
    else:
        st.markdown('<p class="warning-msg">📭 No books in library to edit!</p>', unsafe_allow_html=True)

def delete_book():
    st.markdown('<p class="subheader">🗑️ Delete Book</p>', unsafe_allow_html=True)
    if library:
        selected_title = st.selectbox('📚 Select a book to delete',
                                    [book['title'] for book in library])

        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button('Delete Book 🗑️', use_container_width=True):
                for book in library:
                    if book['title'] == selected_title:
                        library.remove(book)
                        save_library(library)
                        st.markdown('<p class="success-msg">✅ Book deleted successfully!</p>', 
                                  unsafe_allow_html=True)
                        break
    else:
        st.markdown('<p class="warning-msg">📭 No books in library to delete!</p>', unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">📚 Personal Library Manager</h1>', unsafe_allow_html=True)
    
    menu = {
        'View Books 📚': view_books,
        'Add Book ➕': add_book,
        'Edit Book ✏️': edit_book,
        'Delete Book 🗑️': delete_book
    }
    
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        choice = st.selectbox('📋 Menu', list(menu.keys()))
        st.markdown('</div>', unsafe_allow_html=True)

    menu[choice]()

if __name__ == '__main__':
    library = load_library()
    main()
