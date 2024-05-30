import React, { useState } from 'react';
import "./CourseSearch.css";

function CourseSearch() {

  const [loading, setLoading] = useState(false);
  const [school, setSchool] = useState("sjsu")
  const [prompt, setPrompt] = useState("");
  const [recommendations, setRecommendations] = useState([]);

  function getRecommendations(limit) {
    if (prompt === "") {
      setRecommendations([])
    }
    else {
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
            "school": school,
            "user_query": prompt,
            "limit": limit
          })
        }
      )
      .then(response => response.json())
      .then(content => setRecommendations(content['courses']))
      .then(() => setLoading(false));
    }
  }

  return (
    <div className='course-search'>
      <select name="schools" id="schools" onChange={(e) => setSchool(e.target.value)}>
        <option value="sjsu">sjsu</option>
      </select>
      <input 
        id='course-search-bar'
        className={loading ? 'disabled' : ''}
        placeholder='Type something your interested in...' 
        type='text'
        onChange={(e) => setPrompt(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !loading) {
            getRecommendations(5);
          }
        }}
      />
      { loading && <p id='loading-text'>Finding your personalized courses...</p> }
      <ul>
        {
          recommendations.map((course) => {
            return (
              <a href={`https://catalog.sjsu.edu/preview_course_nopop.php?catoid=${course.catoid}&coid=${course.coid}`} target='__blank'>
                <li>
                  <p className='course-code'>{course.course_code}</p>
                  <p>{course.course_description}</p>
                </li>
              </a>
            )
          })
        }
        {
          recommendations.length > 0 && 
          <button id='load-more' className={loading ? 'disabled' : ''} onClick={() => {
            if (!loading) {
              getRecommendations(recommendations.length + 5)
            }
          }}>
            Load More
          </button>
        }
      </ul>
    </div>
  )
}

export default CourseSearch
