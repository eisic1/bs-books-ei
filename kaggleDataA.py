import pandas as pd
import streamlit as st
import plotly.express as px

books_df = pd.read_csv("bestsellers_with_categories_2022_03_27.csv")

st.title("Bestselling Books Analysis")
st.write("This app analyzes the Amazon Top SElling books from 2009 to 2022.")

# Sidebar: Add New Data
st.sidebar.header("Add New Book Data")
with st.sidebar.form("book_form"):
    new_name = st.text_input("Book Name")
    new_author = st.text_input("Author")
    new_user_rating = st.slider("User's Rating", 0.0, 5.0, 0.0, 0.1)
    new_reviews = st.number_input("Reviews", min_value=0, step=1)
    new_price = st.number_input("Price", min_value=0, step=1)
    new_year = st.number_input("Year", min_value=2009, max_value=2022, step=1)
    new_genre = st.selectbox("Genre", books_df["Genre"].unique())
    submit_button = st.form_submit_button(label="Add Book")

if submit_button:
    new_data = {
        "Name": new_name,
        "Author": new_author,
        "User Rating": new_user_rating,
        "Reviews": new_reviews,
        "Price": new_price,
        "Year": new_year,
        "Genre": new_genre
    }
    # Add new data to the top if the DataFrame
    books_df = pd.concat([pd.DataFrame(new_data, index=[0]), books_df], ignore_index=True)
    books_df.to_csv("bestsellers_with_categories_2022_03_27.csv", index=False)
    st.sidebar.success("New Book Added successfully")

# Summary Statistics
st.subheader("Summary Statistics")
total_books = books_df.shape[0]
unique_titles = books_df['Name'].nunique()
average_rating = books_df['User Rating'].mean()
average_price = books_df['Price'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Books", total_books)
col2.metric("Unique Titles", unique_titles)
col3.metric("Average Rating", average_rating)
col4.metric("Average Price", average_price)

# Dataset Preview
st.subheader("Dataset Preview")
st.write(books_df.head())

# Book Title Distribution and Author Distribution
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Book Titles")
    top_titles = books_df['Name'].value_counts().head(10)
    st.bar_chart(top_titles)

with col2:
    st.subheader("Top 10 Authors")
    top_authors = books_df['Author'].value_counts().head(10)
    st.bar_chart(top_authors)

# Genre Distribution Pie Chart
st.subheader("Genre Distribution")
fig = px.pie(books_df, names='Genre', title="Most Liked Genre (2009-2022)",
             color="Genre", color_discrete_sequence=px.colors.sequential.Plasma)

st.plotly_chart(fig)

# Interactivity: Filter Data by Genre
st.subheader("Filter Data by Genre")
genre_filter = st.selectbox("Select Genre", books_df['Genre'].unique())
filtered_df = books_df[books_df['Genre'] == genre_filter]
st.write(filtered_df)
