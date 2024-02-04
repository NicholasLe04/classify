import React, { useState } from 'react';
import "./CourseSearch.css";

function CourseSearch() {

  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState([]);

  function getRecommendations(prompt) {
    setLoading(true);

    fetch(
      `${process.env.REACT_APP_API_ENDPOINT_BASE}/api/v1/get-courses/`, 
      {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'x-api-key': process.env.REACT_APP_API_KEY
        },
        body: JSON.stringify({
          "user_query": prompt,
          "limit": 5
        })
      }
    )
    .then(response => response.json())
    .then(content => setRecommendations(content['courses']))
    .then(() => setLoading(false));
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
        className={loading ? 'disabled' : ''}
        placeholder='I love to...' 
        type='text'
        onKeyDown={(e) => {
          if (e.key === "Enter" && !loading) {
            handleSearch(e.target.value);
          }
        }}
      />
      { loading && <p id='loading-text'>Finding your personalized courses...</p> }
      <ul>
        {
          recommendations.map((course) => {
            return (
              <a href={`https://catalog.sjsu.edu/preview_course_nopop.php?catoid=${course.course_data.catoid}&coid=${course.course_data.coid}`} target='__blank'>
                <li>
                  <p className='course-code'>{course.course_code}</p>
                  <p>{course.course_data.course_description}</p>
                </li>
              </a>
            )
          })
        }
      </ul>
    </div>
  )
}

export default CourseSearch
