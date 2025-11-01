// API configuration and helper functions for backend communication

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

// Helper function to handle API responses
const handleResponse = async (response) => {
  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(data.error || 'Something went wrong');
  }
  
  return data;
};

// GET all jobs with optional filters
export const getJobs = async (filters = {}) => {
  try {
    const queryParams = new URLSearchParams();
    
    // Add filters to query params
    if (filters.job_type) queryParams.append('job_type', filters.job_type);
    if (filters.location) queryParams.append('location', filters.location);
    if (filters.tag) queryParams.append('tag', filters.tag);
    if (filters.search) queryParams.append('search', filters.search);
    if (filters.sort) queryParams.append('sort', filters.sort);
    
    const url = `${API_BASE_URL}/jobs${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Error fetching jobs:', error);
    throw error;
  }
};

// GET single job by ID
export const getJobById = async (jobId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Error fetching job:', error);
    throw error;
  }
};

// POST - Create new job
export const createJob = async (jobData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/jobs`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(jobData),
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Error creating job:', error);
    throw error;
  }
};

// PUT/PATCH - Update existing job
export const updateJob = async (jobId, jobData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(jobData),
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Error updating job:', error);
    throw error;
  }
};

// DELETE - Delete job
export const deleteJob = async (jobId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Error deleting job:', error);
    throw error;
  }
};

export default {
  getJobs,
  getJobById,
  createJob,
  updateJob,
  deleteJob,
};