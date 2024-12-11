import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { Spinner, Button, Alert, Table } from 'react-bootstrap';
import { BackendAPI } from '../api';
import { useAuth } from '../context/AuthContext';

const ProfilePage = () => {
    const { user } = useAuth();
    const [profile, setProfile] = useState(null);
    const [bookings, setBookings] = useState([]);
    const [userHotelsBookings, setUserHotelsBookings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const location = useLocation();
    const { state } = location;

    useEffect(() => {
        const fetchData = async () => {
            try {
                const profileResponse = await BackendAPI.get('/profiles/me/');
                setProfile(profileResponse.data);
    
                const userBookingsResponse = await BackendAPI.get('/bookings/me/');
                setBookings(userBookingsResponse.data);
    
                if (user?.groups?.includes('Tenant')) {
                    const ownerBookingsResponse = await BackendAPI.get('/bookings/owner/');
                    setUserHotelsBookings(ownerBookingsResponse.data);
                }
            } catch (error) {
                setError('Failed to load data');
                console.error(error);
            } finally {
                setLoading(false);
            }
        };
    
        fetchData();
    }, []);

    const handleUpdateClick = () => navigate('/profile/update');

    const handleCancelBooking = async (bookingId) => {
        try {
            await BackendAPI.patch(`/bookings/${bookingId}/`, { status: 'cancelled' });
            setUserHotelsBookings((prevBookings) =>
                prevBookings.map((booking) => (
                    booking.id === bookingId ? { ...booking, status: 'cancelled' } : booking
                ))
            );
        } catch (err) {
            console.error('Failed to cancel booking', err);
        }
    };

    const handleConfirmBooking = async (bookingId) => {
        try {
            await BackendAPI.patch(`/bookings/${bookingId}/`, { status: 'confirmed' });
            setUserHotelsBookings((prevBookings) =>
                prevBookings.map((booking) => (
                    booking.id === bookingId ? { ...booking, status: 'confirmed' } : booking
                ))
            );
        } catch (err) {
            console.error('Failed to confirm booking', err);
        }
    };
    
    const handleRejectBooking = async (bookingId) => {
        try {
            await BackendAPI.patch(`/bookings/${bookingId}/`, { status: 'rejected' });
            setUserHotelsBookings((prevBookings) =>
                prevBookings.map((booking) => (
                    booking.id === bookingId ? { ...booking, status: 'rejected' } : booking
                ))
            );
        } catch (err) {
            console.error('Failed to reject booking', err);
        }
    };

    if (loading) return <Spinner animation="border" variant="primary" />;
    if (error) return <p className="text-danger">{error}</p>;

    return (
        <div className="container mt-4">
            <h1 className="mb-4">Profile</h1>
            {state?.successMessage && <Alert variant="success">{state.successMessage}</Alert>}
            {state?.errorMessage && <Alert variant="danger">{state.errorMessage}</Alert>}
            {profile && (
                <div className="card">
                    <div className="card-body">
                        <h5 className="card-title">Username: {profile.username}</h5>
                        <p className="card-text"><strong>Bio:</strong> {profile.bio || 'No bio provided'}</p>
                        <p className="card-text"><strong>Birth Date:</strong> {profile.birth_date || 'Not specified'}</p>
                        <p className="card-text"><strong>Location:</strong> {profile.location || 'Not specified'}</p>
                        <p className="card-text"><strong>Total Bookings:</strong> {profile.total_bookings || '0'}</p>
                        {profile.profile_picture && (
                            <img
                                src={profile.profile_picture}
                                alt="Profile"
                                className="img-fluid rounded-circle"
                                style={{ maxWidth: '150px' }}
                            />
                        )}
                        <div className="mt-3">
                            <Button variant="primary" onClick={handleUpdateClick}>
                                Update Profile
                            </Button>
                        </div>
                    </div>
                </div>
            )}

            <h2 className="mt-5">My Bookings</h2>
            {bookings.length > 0 ? (
                <Table striped bordered hover responsive>
                    <tbody>
                        {bookings.map((booking) => (
                            <tr key={booking.id}>
                                <td>
                                    <div className="d-flex flex-column align-items-center">
                                        <Link to={`/hotels/${booking.room.hotel}/rooms/${booking.room.id}`}>
                                            <img
                                                src={booking.room.preview_image}
                                                alt="Room Preview"
                                            />
                                        </Link>
                                    </div>
                                </td>
                                <td>
                                    <div>
                                        <Link to={`/hotels/${booking.room.hotel}/rooms/${booking.room.id}`} className="btn">
                                            <p><strong>{booking.room.hotel_name} - {booking.room.name}</strong></p>
                                            <p>{booking.room.hotel_type} - {booking.room.type}</p>
                                            <p>{booking.room.country}, {booking.room.city}, {booking.room.address}</p>
                                            <p><strong>Price per night:</strong> ${booking.room.price_per_night}</p>
                                        </Link>
                                    </div>
                                </td>
                                <td>
                                    <p><strong>Start Date:</strong> {booking.start_date}</p>
                                    <p><strong>End Date:</strong> {booking.end_date}</p>
                                    <p><strong>Total Price:</strong> ${booking.room.price_per_night * Math.ceil((new Date(booking.end_date) - new Date(booking.start_date)) / (1000 * 60 * 60 * 24))}</p>
                                    <p><strong>Status:</strong> {booking.status}</p>
                                    {booking.status !== 'cancelled' && booking.status !== 'rejected' && (
                                        <Button variant="danger" size="sm" onClick={() => handleCancelBooking(booking.id)}>
                                            Cancel Booking
                                        </Button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            ) : (
                <p>No bookings found</p>
            )}
            {user?.groups?.includes('Tenant') && (
                <>
                    <h2 className="mt-5">My Room's Bookings</h2>
                    {userHotelsBookings.length > 0 ? (
                        <Table striped bordered hover responsive>
                            <tbody>
                                {userHotelsBookings.map((booking) => (
                                    <tr key={booking.id}>
                                            <td>
                                                <div className="d-flex flex-column align-items-center">
                                                    <Link to={`/hotels/${booking.room.hotel}/rooms/${booking.room.id}`}>
                                                        <img
                                                            src={booking.room.preview_image}
                                                            alt="Room Preview"
                                                        />
                                                    </Link>
                                                </div>
                                            </td>
                                            <td>
                                                <div>
                                                    <Link to={`/hotels/${booking.room.hotel}/rooms/${booking.room.id}`} className="btn">
                                                        <p><strong>{booking.room.hotel_name} - {booking.room.name}</strong></p>
                                                        <p>{booking.room.hotel_type} - {booking.room.type}</p>
                                                        <p>{booking.room.country}, {booking.room.city}, {booking.room.address}</p>
                                                        <p><strong>Price per night:</strong> ${booking.room.price_per_night}</p>
                                                    </Link>
                                                </div>
                                            </td>
                                        <td>
                                            <p><strong>Start Date:</strong> {booking.start_date}</p>
                                            <p><strong>End Date:</strong> {booking.end_date}</p>
                                            <p><strong>Total Price:</strong> ${booking.room.price_per_night * Math.ceil((new Date(booking.end_date) - new Date(booking.start_date)) / (1000 * 60 * 60 * 24))}</p>
                                            <p><strong>Status:</strong> {booking.status}</p>
                                            <p><strong>User:</strong> {booking.user.email}</p>
                                            {booking.status === 'active' && (
                                                <>
                                                    <Button
                                                        variant="success"
                                                        size="sm"
                                                        onClick={() => handleConfirmBooking(booking.id)}
                                                    >
                                                        Confirm
                                                    </Button>
                                                    <Button
                                                        variant="danger"
                                                        size="sm"
                                                        onClick={() => handleRejectBooking(booking.id)}
                                                    >
                                                        Reject
                                                    </Button>
                                                </>
                                            )}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </Table>
                    ) : (
                        <p>No bookings found</p>
                    )}
                </>
            )}
        </div>
    );
};

export default ProfilePage;
