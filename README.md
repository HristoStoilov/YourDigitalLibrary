# Digital Library Web Application

A Flask-based web application for managing a digital book library with user authentication, book catalog, and review system.

## Features

### Phase 1 - Core Features ✅
- **User Registration & Authentication**: Secure user registration, login, and logout
- **User Profile Management**: View and manage user profiles
- **Book CRUD Operations**: Create, read, update, and delete books
- **Book Catalogue**: Browse books with search and filtering capabilities
- **Book Reviews & Ratings**: Users can add reviews and ratings to books

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login for session management
- **Security**: Werkzeug for password hashing
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with responsive design

## Installation

1. **Clone or download the project**
   ```bash
   cd YourDigitalLibrary
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   env\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://127.0.0.1:5000`

## Project Structure

```
YourDigitalLibrary/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── library.db            # SQLite database (created automatically)
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── profile.html
│   ├── books.html
│   ├── book_detail.html
│   ├── add_book.html
│   └── edit_book.html
└── static/               # Static files
    ├── css/
    │   └── style.css
    ├── js/
    │   └── app.js
    └── img/
```

## Database Models

### User
- id: Primary key
- username: Unique username
- email: Unique email address
- password_hash: Hashed password
- created_at: Registration timestamp
- profile_picture: Optional profile image URL
- bio: Optional user biography

### Book
- id: Primary key
- title: Book title
- author: Book author
- isbn: ISBN number (optional)
- description: Book description
- published_date: Publication date
- cover_image: Cover image URL (optional)
- created_at: Creation timestamp

### Review
- id: Primary key
- rating: Star rating (1-5)
- comment: Review text
- created_at: Review timestamp
- user_id: Foreign key to User
- book_id: Foreign key to Book

## API Endpoints

### Authentication
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout

### Books
- `GET /books` - Book catalogue with search/filter
- `GET /book/<id>` - Book details
- `GET/POST /add_book` - Add new book (authenticated)
- `GET/POST /edit_book/<id>` - Edit book (authenticated)
- `POST /delete_book/<id>` - Delete book (authenticated)

### Reviews
- `POST /add_review/<book_id>` - Add review to book (authenticated)

### User
- `GET /profile` - User profile (authenticated)

## Security Features

- Password hashing using Werkzeug
- Session-based authentication with Flask-Login
- CSRF protection
- SQL injection prevention with SQLAlchemy
- Input validation on forms

## Development

### Running in Debug Mode
The application runs in debug mode by default, which provides:
- Automatic server restart on code changes
- Detailed error pages
- Interactive debugger

### Database Management
The SQLite database is created automatically when the app first runs. To reset the database:
1. Delete `library.db`
2. Restart the application

## Future Enhancements (Phase 2+)

- User roles and permissions
- Book borrowing/lending system
- Advanced search with filters
- Book recommendations
- Social features (following users, sharing reviews)
- API endpoints for mobile app
- File upload for book covers
- Email notifications
- Admin dashboard

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.