# Hotel Booking Platform

## Overview
This project is a full-stack web application designed for hotel booking. It allows users to search, book, and manage hotel reservations while enabling hotel owners to list and manage their properties. The application is structured into three main components:

1. **Backend**: Built with Django, providing RESTful APIs for authentication, profile management, hotel listings, room details, and bookings.
2. **Frontend**: Developed using React, delivering a responsive and intuitive user interface for end-users.
3. **API Gateway**: Configured with Nginx, acting as a reverse proxy for routing requests to the appropriate services.

---

## Features
### Backend
- **Authentication**: Custom user model with secure authentication and authorization.
- **Profile Management**: CRUD operations for user profiles.
- **Hotel and Room Management**: APIs for creating, reading, updating, and deleting hotels and rooms.
- **Booking Management**: Booking system with support for user reservations.
- **Media Handling**: Serve and manage uploaded media files.

### Frontend
- **Routing**: Dynamic routing for various pages including home, hotels, rooms, and profile management.
- **Authentication Flows**: Login, registration, and logout functionality.
- **User Dashboard**: Manage bookings and profiles.
- **Search and Filter**: Search hotels and filter rooms based on user preferences.

### API Gateway
- **Reverse Proxy**: Routes API and static file requests to the backend or frontend.
- **Access Control**: Limits access to admin and API endpoints using referrer checks.
- **Static File Hosting**: Serves React frontend build files.

---

## Project Structure

### Backend
#### Main Configurations
- **URL Configuration**:
  ```python
  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/auth/', include('auth_app.urls')),
      path('api/profiles/', include('profiles.urls')),
      path('api/hotels/', include('hotels.urls')),
      path('api/rooms/', include('rooms.urls')),
      path('api/bookings/', include('bookings.urls')),
  ]
  ```
- **Installed Apps**: Includes `rest_framework`, `corsheaders`, and custom apps (`auth_app`, `profiles`, `hotels`, `rooms`, `bookings`).

#### Settings
- Environment variables are managed using `.env`.
- Database: Configured for MySQL.
- Media: Static and media file handling.

### Frontend
#### File Structure
- **Pages**:
  - `HomePage`: Main landing page.
  - `HotelList`, `HotelDetails`, `RoomDetails`: Hotel and room browsing.
  - `ProfilePage`, `UpdateProfilePage`: User management.
  - `LoginPage`, `RegistrationPage`, `LogoutPage`: Authentication.
- **Components**:
  - `Header` and `Footer`: Common layout components.

#### Main Configuration
```jsx
function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="d-flex flex-column min-vh-100">
          <Header />
          <main className="flex-grow-1">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/hotels" element={<HotelList />} />
              <Route path="/hotels/:hotel_id" element={<HotelDetails />} />
              {/* Additional routes */}
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </AuthProvider>
  );
}
export default App;
```

### API Gateway
#### Nginx Configuration
- Reverse proxy routes:
  - `/admin/` -> Backend admin interface.
  - `/api/` -> Backend APIs.
  - `/media/` -> Media files.
  - `/` -> React frontend.
- Example:
  ```nginx
  location /api/ {
      proxy_pass http://backend/api/;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
  }
  ```

---

## Getting Started

### Prerequisites
- **Backend**: Python 3.10+, Django, MySQL.
- **Frontend**: Node.js 16+, npm/yarn.
- **API Gateway**: Nginx.

### Installation
#### Backend
1. Clone the repository and navigate to the backend directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up `.env` file with environment variables.
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

#### Frontend
1. Navigate to the frontend directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

#### Nginx
1. Configure Nginx using the provided configuration file.
2. Restart the Nginx service:
   ```bash
   sudo service nginx restart
   ```

---

## Deployment
- Use Docker to containerize the backend, frontend, and Nginx.
- Configure CI/CD pipelines for automated testing and deployment.

---

## License
This project is licensed under the MIREA License.

## Deploy status
Currently runnung on 178.253.43.254 ip addres - check it out