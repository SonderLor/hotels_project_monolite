import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { BackendAPI } from '../api';
import { useAuth } from '../context/AuthContext';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const RoomDetails = () => {
    const { hotel_id, room_id } = useParams();
    const [room, setRoom] = useState(null);
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const { user, isLoadingUser } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchRoomDetails = async () => {
            try {
                const response = await BackendAPI.get(`/rooms/rooms/${room_id}/`);
                setRoom(response.data);
            } catch (error) {
                console.error('Failed to fetch room details:', error);
            }
        };

        fetchRoomDetails();
    }, [room_id]);

    const handleBooking = async () => {
        if (!startDate || !endDate) {
            setError('Please select both start and end dates.');
            return;
        }

        setLoading(true);
        setError('');
        try {
            const user_id = user.id;
            BackendAPI.post('bookings/', {
                user_id: user_id,
                room_id: room.id,
                start_date: startDate.toISOString().split('T')[0],
                end_date: endDate.toISOString().split('T')[0],
                status: "active",
            });
            navigate('/profile');
        } catch (err) {
            setError('Failed to book the room. Please try again.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (isLoadingUser) return <div>Loading user data...</div>;

    if (!room) return <div>Loading room data...</div>;

    return (
        <div className="container mt-5">
            <h1 className="mb-4">{room.name}</h1>
            <p>{room.country}, {room.city}, {room.address}</p>
            <p>Hotel: {room.hotel_name}, {room.hotel_type}</p>
            <p>Room: {room.name}, {room.type}</p>
            <p>Price per night: ${room.price_per_night}</p>
            <p>{room.is_available ? 'Available' : 'Not Available'}</p>
            <p>Total Bookings: {room.total_bookings}</p>

            <h2 className="mt-4">Gallery</h2>
            {room?.images && room.images.length > 0 ? (
                <div className="d-flex flex-wrap">
                    {room.images.map((image) => (
                        <div key={image.id} className="m-2">
                            <img
                                src={image.image}
                                alt={`Room ${room.name}`}
                                className="img-thumbnail"
                                style={{ maxWidth: '150px' }}
                            />
                        </div>
                    ))}
                </div>
            ) : (
                <p>No images available for this room.</p>
            )}

            <div className="mt-4">
                <h2>Book this Room</h2>
                <div className="d-flex gap-3">
                    <DatePicker
                        selected={startDate}
                        onChange={(date) => setStartDate(date)}
                        selectsStart
                        startDate={startDate}
                        endDate={endDate}
                        placeholderText="Start Date"
                        className="form-control"
                    />
                    <DatePicker
                        selected={endDate}
                        onChange={(date) => setEndDate(date)}
                        selectsEnd
                        startDate={startDate}
                        endDate={endDate}
                        placeholderText="End Date"
                        className="form-control"
                        minDate={startDate}
                    />
                </div>
                {error && <p className="text-danger mt-2">{error}</p>}
                <button
                    className="btn btn-primary mt-3"
                    onClick={handleBooking}
                    disabled={loading}
                >
                    {loading ? 'Booking...' : 'Book Now'}
                </button>
            </div>

            <Link to={`/hotels/${hotel_id}`} className="btn btn-secondary mt-4">
                Back to Hotel
            </Link>
        </div>
    );
};

export default RoomDetails;
