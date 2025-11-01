import React, { useState, useEffect } from 'react';
import './JobForm.css';

const JobForm = ({ jobToEdit, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    location: '',
    posting_date: 'Just posted',
    job_type: 'Full-time',
    tags: ''
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Populate form if editing
  useEffect(() => {
    if (jobToEdit) {
      setFormData({
        title: jobToEdit.title || '',
        company: jobToEdit.company || '',
        location: jobToEdit.location || '',
        posting_date: jobToEdit.posting_date || 'Just posted',
        job_type: jobToEdit.job_type || 'Full-time',
        tags: Array.isArray(jobToEdit.tags) ? jobToEdit.tags.join(', ') : jobToEdit.tags || ''
      });
    }
  }, [jobToEdit]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
    
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: ''
      });
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Required field validation
    if (!formData.title.trim()) {
      newErrors.title = 'Job title is required';
    }

    if (!formData.company.trim()) {
      newErrors.company = 'Company name is required';
    }

    if (!formData.location.trim()) {
      newErrors.location = 'Location is required';
    }

    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    const newErrors = validateForm();
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsSubmitting(true);

    try {
      // Process tags - convert to array if comma-separated string
      const processedData = {
        ...formData,
        tags: formData.tags ? formData.tags.split(',').map(tag => tag.trim()) : []
      };

      await onSubmit(processedData);
      
      // Reset form on successful submission (only for new jobs, not edits)
      if (!jobToEdit) {
        setFormData({
          title: '',
          company: '',
          location: '',
          posting_date: 'Just posted',
          job_type: 'Full-time',
          tags: ''
        });
      }
      
      setErrors({});
    } catch (error) {
      setErrors({
        submit: error.message || 'Failed to save job. Please try again.'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="job-form-container">
      <div className="job-form-header">
        <h2>{jobToEdit ? 'Edit Job' : 'Add New Job'}</h2>
        {onCancel && (
          <button 
            className="close-btn" 
            onClick={onCancel}
            aria-label="Close form"
          >
            ✕
          </button>
        )}
      </div>

      <form onSubmit={handleSubmit} className="job-form">
        {/* Job Title */}
        <div className="form-group">
          <label htmlFor="title">
            Job Title <span className="required">*</span>
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="e.g. Senior Actuary"
            className={errors.title ? 'error' : ''}
          />
          {errors.title && <span className="error-message">{errors.title}</span>}
        </div>

        {/* Company */}
        <div className="form-group">
          <label htmlFor="company">
            Company Name <span className="required">*</span>
          </label>
          <input
            type="text"
            id="company"
            name="company"
            value={formData.company}
            onChange={handleChange}
            placeholder="e.g. XYZ Insurance"
            className={errors.company ? 'error' : ''}
          />
          {errors.company && <span className="error-message">{errors.company}</span>}
        </div>

        {/* Location */}
        <div className="form-group">
          <label htmlFor="location">
            Location <span className="required">*</span>
          </label>
          <input
            type="text"
            id="location"
            name="location"
            value={formData.location}
            onChange={handleChange}
            placeholder="e.g. London, UK or Remote"
            className={errors.location ? 'error' : ''}
          />
          {errors.location && <span className="error-message">{errors.location}</span>}
        </div>

        <div className="form-row">
          {/* Job Type */}
          <div className="form-group">
            <label htmlFor="job_type">Job Type</label>
            <select
              id="job_type"
              name="job_type"
              value={formData.job_type}
              onChange={handleChange}
            >
              <option value="Full-time">Full-time</option>
              <option value="Part-time">Part-time</option>
              <option value="Contract">Contract</option>
              <option value="Internship">Internship</option>
            </select>
          </div>

          {/* Posting Date */}
          <div className="form-group">
            <label htmlFor="posting_date">Posting Date</label>
            <input
              type="text"
              id="posting_date"
              name="posting_date"
              value={formData.posting_date}
              onChange={handleChange}
              placeholder="e.g. 2 days ago, Just posted"
            />
          </div>
        </div>

        {/* Tags */}
        <div className="form-group">
          <label htmlFor="tags">
            Tags/Keywords
            <span className="help-text">(comma-separated)</span>
          </label>
          <input
            type="text"
            id="tags"
            name="tags"
            value={formData.tags}
            onChange={handleChange}
            placeholder="e.g. Life, Health, Pricing, Python"
          />
          <small className="field-hint">
            Enter tags separated by commas (e.g., Life, Health, Pricing)
          </small>
        </div>

        {/* Submit Error */}
        {errors.submit && (
          <div className="form-error">
            {errors.submit}
          </div>
        )}

        {/* Form Actions */}
        <div className="form-actions">
          {onCancel && (
            <button 
              type="button" 
              className="btn-cancel"
              onClick={onCancel}
              disabled={isSubmitting}
            >
              Cancel
            </button>
          )}
          <button 
            type="submit" 
            className="btn-submit"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Saving...' : (jobToEdit ? 'Update Job' : 'Add Job')}
          </button>
        </div>
      </form>
    </div>
  );
};

export default JobForm;