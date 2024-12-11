import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { BackendAPI } from '../api';

const SearchPage = () => {
    const [searchCriteria, setSearchCriteria] = useState({
        hotel: '',
        room: '',
        hotel_type: '',
        room_type: '',
        country: '',
        city: '',
        priceMin: '',
        priceMax: '',
        sort: '',
        startDate: null,
        endDate: null,
    });
    const [results, setResults] = useState({ hotels: [], rooms: [] });
    const [roomTypes, setRoomTypes] = useState([]);
    const [hotelTypes, setHotelTypes] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [showRoomsOnly, setShowRoomsOnly] = useState(false);

    useEffect(() => {
        const fetchTypes = async () => {
            try {
                const roomTypesResponse = await BackendAPI.get('/rooms/types/');
                const hotelTypesResponse = await BackendAPI.get('/hotels/types/');
                setRoomTypes(roomTypesResponse.data);
                setHotelTypes(hotelTypesResponse.data);
            } catch (error) {
                console.error('Failed to fetch types:', error);
            }
        };

        fetchTypes();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setSearchCriteria((prev) => ({ ...prev, [name]: value }));
    };

    const handleDateChange = (name, date) => {
        setSearchCriteria((prev) => ({ ...prev, [name]: date }));
    };

    const handleToggle = () => {
        setShowRoomsOnly((prev) => !prev);
    };

    const handleSearch = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await BackendAPI.get('/hotels/search/', {
                params: {
                    ...searchCriteria,
                    startDate: searchCriteria.startDate
                        ? searchCriteria.startDate.toISOString().split('T')[0]
                        : null,
                    endDate: searchCriteria.endDate
                        ? searchCriteria.endDate.toISOString().split('T')[0]
                        : null,
                },
            });
            setResults(response.data);
        } catch (err) {
            setError('Failed to load data. Please try again.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mt-5">
            <h1>Search Hotels and Rooms</h1>
            <div className="mb-4">
                <div className="row g-3">
                    <div className="col-md-3">
                        <input
                            type="text"
                            name="hotel"
                            placeholder="Hotel Name"
                            className="form-control"
                            value={searchCriteria.hotel}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div className="col-md-3">
                        <input
                            type="text"
                            name="room"
                            placeholder="Room Name"
                            className="form-control"
                            value={searchCriteria.room}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div className="col-md-3">
                        <input
                            type="text"
                            name="country"
                            placeholder="Country"
                            className="form-control"
                            value={searchCriteria.country}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div className="col-md-3">
                        <input
                            type="text"
                            name="city"
                            placeholder="City"
                            className="form-control"
                            value={searchCriteria.city}
                            onChange={handleInputChange}
                        />
                    </div>
                </div>
                <div className="row g-3 mt-3">
                    <div className="col-md-3">
                        <select
                            name="hotel_type"
                            className="form-select"
                            value={searchCriteria.hotel_type}
                            onChange={handleInputChange}
                        >
                            <option value="">Select Hotel Type</option>
                            {hotelTypes.map((type) => (
                                <option key={type.id} value={type.name}>
                                    {type.name}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="col-md-3">
                        <select
                            name="room_type"
                            className="form-select"
                            value={searchCriteria.room_type}
                            onChange={handleInputChange}
                        >
                            <option value="">Select Room Type</option>
                            {roomTypes.map((type) => (
                                <option key={type.id} value={type.name}>
                                    {type.name}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="col-md-3">
                        <DatePicker
                            selected={searchCriteria.startDate}
                            onChange={(date) => handleDateChange('startDate', date)}
                            placeholderText="Start Date"
                            className="form-control"
                            dateFormat="yyyy-MM-dd"
                        />
                    </div>
                    <div className="col-md-3">
                        <DatePicker
                            selected={searchCriteria.endDate}
                            onChange={(date) => handleDateChange('endDate', date)}
                            placeholderText="End Date"
                            className="form-control"
                            dateFormat="yyyy-MM-dd"
                            minDate={searchCriteria.startDate}
                        />
                    </div>
                </div>
                <div className="row g-3 mt-3">
                    <div className="col-md-3">
                        <input
                            type="number"
                            name="priceMin"
                            placeholder="Min Price"
                            className="form-control"
                            value={searchCriteria.priceMin}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div className="col-md-3">
                        <input
                            type="number"
                            name="priceMax"
                            placeholder="Max Price"
                            className="form-control"
                            value={searchCriteria.priceMax}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div className="col-md-3">
                        <select
                            name="sort"
                            className="form-select"
                            value={searchCriteria.sort}
                            onChange={handleInputChange}
                        >
                            <option value="">Sort by</option>
                            <option value="price_per_night">Price: Low to High</option>
                            <option value="-price_per_night">Price: High to Low</option>
                        </select>
                    </div>
                    <div className="col-md-3 d-flex align-items-center">
                        <label className="form-check-label me-2">Show Rooms Only</label>
                        <input
                            type="checkbox"
                            className="form-check-input"
                            checked={showRoomsOnly}
                            onChange={handleToggle}
                        />
                    </div>
                </div>
                <div className="mt-4">
                    <button
                        className="btn btn-primary w-100"
                        onClick={handleSearch}
                        disabled={loading}
                    >
                        {loading ? 'Searching...' : 'Search'}
                    </button>
                </div>
            </div>

            {error && <div className="alert alert-danger">{error}</div>}

            <div className="row">
                {!showRoomsOnly &&
                    results.hotels.map((hotel) => (
                        <div key={hotel.id} className="col-md-4 mb-4">
                            <div className="card">
                                {hotel.preview_image && (
                                    <img
                                        src={hotel.preview_image}
                                        alt={hotel.name}
                                        className="card-img-top"
                                    />
                                )}
                                <div className="card-body">
                                    <h5 className="card-title">{hotel.name}</h5>
                                    <p>City: {hotel.city}</p>
                                    <p>Country: {hotel.country}</p>
                                    <p>Type: {hotel.type}</p>
                                    <Link to={`/hotels/${hotel.id}`} className="btn btn-primary w-100">
                                        View Hotel
                                    </Link>
                                </div>
                            </div>
                        </div>
                    ))}
                {results.rooms.map((room) => (
                    <div key={room.id} className="col-md-4 mb-4">
                        <div className="card">
                            {room.preview_image && (
                                <img
                                    src={room.preview_image}
                                    alt={room.name}
                                    className="card-img-top"
                                />
                            )}
                            <div className="card-body">
                                <h5 className="card-title">{room.name}</h5>
                                <p>{room.country}, {room.city}, {room.address}</p>
                                <p>{room.type}</p>
                                <p>Price per night: ${room.price_per_night}</p>
                                <p>Availability: {room.is_available ? 'Available' : 'Unavailable'}</p>
                                <Link
                                    to={`/hotels/${room.hotel}/rooms/${room.id}`}
                                    className="btn btn-primary w-100"
                                >
                                    View Room
                                </Link>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SearchPage;
