import React, { useState } from 'react';
import "./CourseSearch.css";

function CourseSearch() {

  const [recommendations, setRecommendations] = useState([]);

  function getRecommendations(prompt) {
    fetch(
      `${process.env.REACT_APP_API_ENDPOINT_BASE}/api/v1/get-courses`, 
      {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "user_query": prompt,
          "limit": 5
        })
      }
    )
    .then(response => response.json())
    .then(content => setRecommendations(content['courses']))
  }

  function handleSearch(prompt) {
    if (prompt === "") {
      setRecommendations([])
      return
    }
    getRecommendations(prompt);
  }

  return (
    <div className='course-search'>
      <input 
        id='course-search-bar'
        placeholder='I love to...' 
        type='text'
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleSearch(e.target.value);
          }
        }}
      />
      <ul>
        {
          recommendations.map((course) => {
            return (
              <li>
                <p className='course-code'>{course.course_code}</p>
                <p>{course.course_description}</p>
              </li>
            )
          })
        }
      </ul>
    </div>
  )
}

export default CourseSearch