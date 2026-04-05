/**
 * @module mockData
 * @description Comprehensive mock data engine providing realistic, randomized data structures
 * for the JOBFOR platform, enabling completely standalone frontend operations.
 */

const getRandomElement = (arr) => arr[Math.floor(Math.random() * arr.length)];
const getRandomInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

const COMPANIES = [
    { name: 'TechNova Solutions', logo: 'https://api.dicebear.com/7.x/initials/svg?seed=TN' },
    { name: 'Global Health Care', logo: 'https://api.dicebear.com/7.x/initials/svg?seed=GH' },
    { name: 'EcoStream Energy', logo: 'https://api.dicebear.com/7.x/initials/svg?seed=ES' },
    { name: 'Swift Logistics', logo: 'https://api.dicebear.com/7.x/initials/svg?seed=SL' },
    { name: 'Stellar FinTech', logo: 'https://api.dicebear.com/7.x/initials/svg?seed=SF' },
    { name: 'CloudPeak Systems', logo: 'https://api.dicebear.com/7.x/initials/svg?seed=CP' },
];

const LOCATIONS = ['Bangalore, KA', 'Mumbai, MH', 'Delhi, NCR', 'Hyderabad, TS', 'Pune, MH', 'Remote'];
const JOB_TYPES = ['Full-time', 'Contract', 'Part-time', 'Internship'];
const EXPERIENCE_LEVELS = ['Junior', 'Mid-level', 'Senior', 'Lead'];
const SKILLS = ['React', 'Node.js', 'Python', 'AWS', 'JavaScript', 'SQL', 'TypeScript', 'Docker', 'Machine Learning', 'GraphQL'];

/**
 * Generates a singular realistic job object.
 * 
 * @param {string} id - Explicit ID or generated UUID if omitted.
 * @returns {object}
 */
export const generateJob = (id = `job-${Math.random().toString(36).substr(2, 9)}`) => {
    const company = getRandomElement(COMPANIES);
    return {
        id,
        title: getRandomElement(['Software Engineer', 'Frontend Developer', 'Backend Architect', 'Data Scientist', 'Product Manager', 'DevOps Specialist']),
        company: company.name,
        companyLogo: company.logo,
        location: getRandomElement(LOCATIONS),
        isRemote: Math.random() > 0.7,
        type: getRandomElement(JOB_TYPES),
        experience: getRandomElement(EXPERIENCE_LEVELS),
        salaryMin: getRandomInt(8, 20) * 100000,
        salaryMax: getRandomInt(25, 60) * 100000,
        currency: 'INR',
        postedAt: new Date(Date.now() - getRandomInt(0, 30) * 24 * 60 * 60 * 1000).toISOString(),
        description: 'We are looking for a passionate individual to join our growing team...',
        requirements: ['3+ years of experience', 'Strong communication skills', 'Expert in relevant technologies'],
        skills: Array.from({ length: 4 }, () => getRandomElement(SKILLS)).filter((v, i, a) => a.indexOf(v) === i),
        applyUrl: '#'
    };
};

/**
 * Mocks the complete user profile.
 */
export const mockUser = {
    id: 1,
    email: 'wasim@example.com',
    firstName: 'Wasim',
    lastName: 'Akhtar',
    role: 'PREMIUM',
    avatarUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Wasim',
    headline: 'Senior Full Stack Developer & AI Enthusiast',
    summary: 'Experienced developer with a passion for building scalable applications and integrating AI solutions.',
    phone: '+91 98765 43210',
    preferredLocations: ['Bangalore', 'Remote', 'Hyderabad'],
    experienceYears: 6,
    skills: [
        { id: 1, name: 'React', proficiency: 'Expert' },
        { id: 2, name: 'Node.js', proficiency: 'Advanced' },
        { id: 3, name: 'Python', proficiency: 'Intermediate' }
    ],
    experience: [
        {
            id: 1,
            company: 'Stellar FinTech',
            title: 'Lead Frontend Developer',
            startDate: '2021-03-01',
            isCurrent: true,
            description: 'Leading the development of the primary trading platform.'
        }
    ]
};

/**
 * Mocks application history.
 */
export const mockApplications = Array.from({ length: 5 }, (_, i) => ({
    id: i + 1,
    jobId: `job-${i}`,
    jobData: generateJob(`job-${i}`),
    status: getRandomElement(['APPLIED', 'SCREENING', 'INTERVIEWING', 'OFFERED', 'REJECTED']),
    appliedAt: new Date(Date.now() - i * 5 * 24 * 60 * 60 * 1000).toISOString(),
}));

/**
 * Mocks salary insights.
 */
export const mockSalaryInsights = {
    average: 2400000,
    min: 1200000,
    max: 4800000,
    percentiles: { p10: 1500000, p50: 2400000, p90: 4200000 },
    currency: 'INR',
    roles: [
        { title: 'Frontend Developer', avg: 1800000 },
        { title: 'Backend Developer', avg: 2000000 },
        { title: 'Full Stack Developer', avg: 2200000 }
    ]
};

/**
 * Mocks AI Coach responses.
 */
export const mockAIResponses = {
    analysis: {
        score: 85,
        summary: "Your profile is highly competitive for Senior Frontend roles.",
        strengths: ["Strong React background", "Experience with cross-functional teams"],
        gaps: ["Could improve Cloud expertise (AWS/GCP)", "Limited testing coverage in past projects"]
    },
    chat: (msg) => {
        if (msg.toLowerCase().includes('salary')) return "Based on your experience, you should target a range between 25-35 LPA in tier-1 cities.";
        return "I can help you audit your resume or prepare for technical interviews. What would you like to focus on?";
    }
};

/**
 * Mocks notifications.
 */
export const mockNotifications = [
    { id: 1, type: 'JOB_ALERT', title: 'New Job Matching Your Profile', message: 'Swift Logistics is hiring a Senior Frontend Engineer.', createdAt: new Date().toISOString(), isRead: false },
    { id: 2, type: 'APPLICATION_UPDATE', title: 'Application Status Update', message: 'Your application for EcoStream Energy has moved to "Interviewing".', createdAt: new Date(Date.now() - 3600000).toISOString(), isRead: true }
];
