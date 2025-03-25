'use client';

import { useState } from 'react';

export default function Home() {
    const [query, setQuery] = useState('');
    const [imageSrcs, setImageSrcs] = useState<string[]>([]);
    const [isListening, setIsListening] = useState(false); // State for listening status

    const handleSearch = async (textQuery: string) => { // Accept textQuery as argument
        if (!textQuery) {
            alert('Please enter a search query.');
            return;
        }

        const formData = new FormData();
        formData.append('text_query', textQuery); // Use the textQuery argument

        try {
            const response = await fetch('http://localhost:8000/search/', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log("Response data:", data);

            if (data.image_base64_list && data.image_base64_list.length > 0) {
                setImageSrcs(data.image_base64_list.map((base64: string) => `data:image/jpeg;base64,${base64}`)); // Or PNG and Added type annotation
            } else {
                setImageSrcs([]);
                alert('No results found.');
            }

        } catch (error: any) {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
        }
    };

    const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'Enter') {
            handleSearch(query); // Pass the current query to handleSearch
        }
    };

    const handleVoiceSearch = async () => {
        setIsListening(true); // Update listening state
        try {
            const response = await fetch('http://localhost:8000/voice_search/', {
                method: 'POST',
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log("Voice search response:", data);

            if (data.image_base64_list && data.image_base64_list.length > 0) {
                setImageSrcs(data.image_base64_list.map((base64: string) => `data:image/jpeg;base64,${base64}`)); // Or PNG and Added type annotation
            } else {
                setImageSrcs([]);
                alert('No results found.');
            }

        } catch (error: any) {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
        } finally {
            setIsListening(false); // Reset listening state
        }
    };

    return (
        <div>
            {/* Hero Section */}
            <div className="flex flex-col items-center justify-center h-64 bg-gray-100">
                <h1 className="text-3xl font-bold mb-4">Fashion Product Search</h1>
                <input
                    type="text"
                    placeholder="Search for clothing, accessories, etc..."
                    className="shadow appearance-none border rounded w-96 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={handleKeyDown}
                />
                <button
                    onClick={handleVoiceSearch}
                    disabled={isListening}
                    className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >
                    {isListening ? 'Listening...' : 'Search with Voice'}
                </button>
            </div>

            {/* Image Section - Displayed as a Product Cards */}
            <div className="container mx-auto p-4 flex flex-wrap justify-center">
                {imageSrcs.map((imageSrc, index) => (
                    <div key={index} className="w-64 rounded-md overflow-hidden shadow-md m-2">
                        <img className="w-full object-cover h-64" src={imageSrc} alt={`Product ${index + 1}`} />
                        <div className="px-4 py-2">
                            <div className="font-semibold text-lg text-gray-800 truncate">
                                Product {index + 1}
                            </div>
                            <p className="text-gray-600 text-sm truncate">
                                Short description
                            </p>
                            <p className="text-gray-900 font-medium mt-1">$20.00</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}