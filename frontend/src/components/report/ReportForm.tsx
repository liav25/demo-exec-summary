import { useForm } from 'react-hook-form';
import type { SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { motion } from 'framer-motion';
import { Mail, ChartLine, Calendar, Target, MessageCircle, Sparkles, Shield } from 'lucide-react';
import { useState } from 'react';

interface ReportFormData {
  recipient_email: string;
  report_type: string;
  time_period: string;
  focus_areas: string[];
  specific_questions: string;
}

const schema = yup.object().shape({
  recipient_email: yup.string().email('Invalid email').required('Email is required'),
  report_type: yup.string().required('Report type is required'),
  time_period: yup.string().required('Time period is required'),
  focus_areas: yup.array().of(yup.string().required()).default([]),
  specific_questions: yup.string().default(''),
});

interface ReportFormProps {
  config: {
    report_types: Record<string, { name: string; description: string }>;
    focus_areas: Array<{
      id: string;
      name: string;
      description: string;
      color: string;
      icon: string;
    }>;
  };
  onSubmit: (data: ReportFormData) => void;
  isLoading: boolean;
}

const ReportForm = ({ config, onSubmit, isLoading }: ReportFormProps) => {
  const [selectedFocusAreas, setSelectedFocusAreas] = useState<string[]>([]);
  const { register, handleSubmit, formState: { errors } } = useForm<ReportFormData>({
    resolver: yupResolver(schema),
    defaultValues: {
      focus_areas: [],
      specific_questions: '',
    },
  });

  const handleFormSubmit: SubmitHandler<ReportFormData> = (data) => {
    onSubmit({ ...data, focus_areas: selectedFocusAreas });
  };

  const toggleFocusArea = (area: string) => {
    setSelectedFocusAreas((prev) =>
      prev.includes(area) ? prev.filter((a) => a !== area) : [...prev, area]
    );
  };

  return (
    <div className="form-wrapper">
      <div className="glass-container">
        <form onSubmit={handleSubmit(handleFormSubmit)} className="report-form">
          {/* Basic Information Section */}
          <div className="form-section">
            <h2 className="section-title">
              <Mail size={20} />
              Basic Information
            </h2>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">
                  <Mail size={16} />
                  Executive Email Address
                </label>
                <input
                  type="email"
                  className={`glass-input ${errors.recipient_email ? 'error' : ''}`}
                  placeholder="ceo@company.com"
                  {...register('recipient_email')}
                />
                {errors.recipient_email && (
                  <span className="error-text">{errors.recipient_email.message}</span>
                )}
                <div className="form-text">Report will be delivered to this address</div>
              </div>

              <div className="form-group">
                <label className="form-label">
                  <ChartLine size={16} />
                  Report Type
                </label>
                <select
                  className={`glass-input ${errors.report_type ? 'error' : ''}`}
                  {...register('report_type')}
                >
                  <option value="">Select report type...</option>
                  {Object.entries(config.report_types).map(([key, value]) => (
                    <option key={key} value={key}>
                      {value.name}
                    </option>
                  ))}
                </select>
                {errors.report_type && (
                  <span className="error-text">{errors.report_type.message}</span>
                )}
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">
                  <Calendar size={16} />
                  Analysis Time Period
                </label>
                <select
                  className={`glass-input ${errors.time_period ? 'error' : ''}`}
                  {...register('time_period')}
                >
                  <option value="">Select timeframe...</option>
                  <option value="last_quarter">Last Quarter (90 days)</option>
                  <option value="last_month">Last Month (30 days)</option>
                  <option value="last_6_months">Last 6 Months</option>
                  <option value="ytd">Year to Date</option>
                </select>
                {errors.time_period && (
                  <span className="error-text">{errors.time_period.message}</span>
                )}
              </div>
            </div>
          </div>

          {/* Focus Areas Section */}
          <div className="form-section">
            <h2 className="section-title">
              <Target size={20} />
              Areas of Focus
            </h2>
            <p className="section-description">
              Select the security domains you want emphasized in your report
            </p>

            <div className="focus-pills">
              {config.focus_areas.map((area) => (
                <motion.div
                  key={area.id}
                  className={`focus-pill ${selectedFocusAreas.includes(area.name) ? 'selected' : ''}`}
                  onClick={() => toggleFocusArea(area.name)}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <div className="pill-content">
                    <Shield size={20} />
                    {area.name}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Additional Details Section */}
          <div className="form-section">
            <h2 className="section-title">
              <MessageCircle size={20} />
              Additional Details
            </h2>

            <div className="form-group">
              <label className="form-label">
                Specific Questions or Requirements (Optional)
              </label>
              <textarea
                className="glass-input"
                rows={4}
                placeholder="e.g., What are our top 3 security risks this quarter? How has our phishing success rate changed?"
                {...register('specific_questions')}
              />
              <div className="form-text">
                Include any specific questions or areas you'd like the AI to address
              </div>
            </div>
          </div>

          {/* Submit Section */}
          <div className="submit-section">
            <motion.button
              type="submit"
              className="primary-btn"
              disabled={isLoading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <Sparkles size={20} />
              Generate Security Report
            </motion.button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ReportForm; 