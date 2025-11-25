--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: analysis_history; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.analysis_history (
    id integer NOT NULL,
    user_id integer NOT NULL,
    job_title character varying(200),
    company_name character varying(200),
    compatibility_score double precision NOT NULL,
    compatibility_level character varying(50) NOT NULL,
    resume_text text NOT NULL,
    job_description text NOT NULL,
    analysis_result json NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.analysis_history OWNER TO neondb_owner;

--
-- Name: analysis_history_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.analysis_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.analysis_history_id_seq OWNER TO neondb_owner;

--
-- Name: analysis_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.analysis_history_id_seq OWNED BY public.analysis_history.id;


--
-- Name: email_verifications; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.email_verifications (
    id integer NOT NULL,
    user_id integer NOT NULL,
    token character varying(100) NOT NULL,
    created_at timestamp without time zone,
    expires_at timestamp without time zone NOT NULL,
    is_used boolean
);


ALTER TABLE public.email_verifications OWNER TO neondb_owner;

--
-- Name: email_verifications_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.email_verifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.email_verifications_id_seq OWNER TO neondb_owner;

--
-- Name: email_verifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.email_verifications_id_seq OWNED BY public.email_verifications.id;


--
-- Name: password_resets; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.password_resets (
    id integer NOT NULL,
    user_id integer NOT NULL,
    token character varying(100) NOT NULL,
    created_at timestamp without time zone,
    expires_at timestamp without time zone NOT NULL,
    is_used boolean
);


ALTER TABLE public.password_resets OWNER TO neondb_owner;

--
-- Name: password_resets_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.password_resets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.password_resets_id_seq OWNER TO neondb_owner;

--
-- Name: password_resets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.password_resets_id_seq OWNED BY public.password_resets.id;


--
-- Name: saved_resumes; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.saved_resumes (
    id integer NOT NULL,
    user_id integer NOT NULL,
    title character varying(200) NOT NULL,
    content text NOT NULL,
    is_default boolean NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.saved_resumes OWNER TO neondb_owner;

--
-- Name: saved_resumes_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.saved_resumes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.saved_resumes_id_seq OWNER TO neondb_owner;

--
-- Name: saved_resumes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.saved_resumes_id_seq OWNED BY public.saved_resumes.id;


--
-- Name: test_users; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.test_users (
    id integer,
    username character varying(80),
    email character varying(120),
    password_hash character varying(256),
    first_name character varying(50),
    last_name character varying(50),
    is_verified boolean,
    created_at timestamp without time zone,
    last_login timestamp without time zone
);


ALTER TABLE public.test_users OWNER TO neondb_owner;

--
-- Name: users; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(256) NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    is_verified boolean NOT NULL,
    created_at timestamp without time zone,
    last_login timestamp without time zone
);


ALTER TABLE public.users OWNER TO neondb_owner;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO neondb_owner;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: analysis_history id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.analysis_history ALTER COLUMN id SET DEFAULT nextval('public.analysis_history_id_seq'::regclass);


--
-- Name: email_verifications id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.email_verifications ALTER COLUMN id SET DEFAULT nextval('public.email_verifications_id_seq'::regclass);


--
-- Name: password_resets id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.password_resets ALTER COLUMN id SET DEFAULT nextval('public.password_resets_id_seq'::regclass);


--
-- Name: saved_resumes id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.saved_resumes ALTER COLUMN id SET DEFAULT nextval('public.saved_resumes_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: analysis_history; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.analysis_history (id, user_id, job_title, company_name, compatibility_score, compatibility_level, resume_text, job_description, analysis_result, created_at) FROM stdin;
1	1	Untitled Position	Unknown Company	0.32	Poor Match	PA WA N B H A T T A R A I\r\nSoftware Engineer\r\nAnamnagar , kathmandu\r\n+9779807990779\r\npawaan012@gmail.com\r\n @ https://www.linkedin.com/in/pawanbhattarai/  @ https://github.com/pawanbhattarai/\r\nPassionate software developer with a focus on customer satisfaction, code quality, and teamwork.\r\nExperienced in spearheading software projects and optimizing processes for e ciency.\r\nEX PER IENCE\r\nSoftware Engineer\r\nM.A.P. Tech Pvt. Ltd.\r\nBhaktapur\r\nJul, 2024 - Present\r\nDeveloped and deployed a Rule-based Chatbot using Python and PostgreSQL capable of processing both Devanagari Nepali and\r\nRomanized Nepali input. This chatbot increased user engagement by 20%.\r\nDesigned and implemented an inventory management system for a small/medium business, improving stock accuracy, cost\r\nsavings.\r\nE ectively troubleshooted and resolved production issues, minimizing downtime and ensuring smooth system operation.\r\nSoftware EngineerKathmandu\r\nPhoenix Solution Pv.Ltd.Jul, 2023 - Jun, 2024\r\nLed development and implementation of Government IMS Software, enhancing administrative e ciency.\r\nContributed to design and implementation of University CRM Software, facilitating departmental collaboration.\r\nLed the development and implementation of a Hospital Management System, incorporating the IMIS\r\nSoftware Developer (Intern)\r\nPhoenix Solution Pv.Ltd.\r\nKathmandu\r\nApr, 2023 - Jul, 2023\r\nCollaborated on Government ERP Software, gathering requirements and ensuring compliance.\r\nAssisted in con guring and customizing ERP system for government regulations.\r\nED UCAT IO N\r\nBachelors in Computer Application\r\nTribhuvan University\r\nKathmandu\r\nOct, 2020 - Present\r\nPR O JECT S\r\nStock Predictor\r\nA web application that predicts NEPSE stock prices for the next 3 to 7 trading days.\r\nTechnologies & Tools: Python, Pandas, NumPy, Flask, Selenium, TensorFlow\r\nAlgorithm: Long Short-Term Memory (LSTM)\r\nLink\r\nJsonToSQL/CSV Converter\r\nA platform where users can input JSON data and convert it into either SQL queries or .CSV les according to their needs.\r\nTechnologies and Tools : Spring Boot, JavaScript, HTML, CSS\r\nLink\r\nS K ILLS\r\nSystem Design, Java, Python, PostgreSQL, SQL, Rest Api, Github, NGINX	TechOasis Consulting is seeking an experienced Full Stack Developer to join our development team from Nepal. This role offers the opportunity to work on cutting-edge projects for US clients while enjoying the flexibility of remote work and competitive local compensation.\r\n\r\n\r\nKey ResponsibilitiesDevelopment & Architecture\r\nDesign, develop, and maintain scalable web applications using modern full-stack technologies\r\nBuild responsive, user-friendly frontend interfaces using React or Angular\r\nDevelop robust backend APIs and services using object-oriented programming languages\r\nImplement and maintain database solutions (SQL and NoSQL)\r\nEnsure code quality through testing, code reviews, and best practices\r\n\r\n\r\nCollaboration & Leadership\r\nWork closely with US-based product managers and designers (Central timezone overlap required)\r\nMentor junior developers and contribute to team knowledge sharing\r\nParticipate in agile development processes, including sprint planning and retrospectives\r\nCollaborate with DevOps teams for deployment and infrastructure management\r\n\r\n\r\nTechnical Excellence\r\nOptimize application performance and scalability\r\nImplement security best practices and data protection measures\r\nStay current with emerging technologies and industry trends\r\nContribute to technical documentation and system architecture decisions\r\n\r\n\r\nRequired QualificationsExperience & Education\r\nAround 5 years of professional full-stack development experience\r\nBachelor's degree in Computer Science, Software Engineering, or equivalent practical experience\r\nProven track record of delivering complex web applications from concept to production\r\n\r\n\r\nTechnical Skills - Frontend\r\nExpert proficiency in either React or Angular\r\nStrong knowledge of HTML5, CSS3, and modern JavaScript (ES6+)\r\nExperience with state management libraries (Redux, NgRx, Zustand)\r\nFamiliarity with CSS frameworks (Tailwind CSS, Bootstrap, Material-UI)\r\nUnderstanding of responsive design principles and cross-browser compatibility\r\n\r\n\r\nTechnical Skills - Backend\r\nStrong proficiency in any one object-oriented programming language:\r\nJava (Spring Boot, Spring Framework)\r\nC# (.NET Core, ASP.NET)\r\nPython (Django, FastAPI, Flask)\r\nNode.js (Express, Nest.js)\r\nExperience with RESTful API design and implementation\r\nKnowledge of database design and optimization (PostgreSQL, MySQL, MongoDB)\r\nUnderstanding of authentication and authorization mechanisms (JWT, OAuth)\r\n\r\n\r\nAdditional Technical Requirements\r\nProficiency with version control systems (Git, GitHub/GitLab)\r\nExperience with cloud platforms (AWS, Azure, or GCP)\r\nKnowledge of containerization technologies (Docker)\r\nFamiliarity with CI/CD pipelines and DevOps practices\r\nUnderstanding of testing frameworks and methodologies\r\n\r\n\r\nSoft Skills & Communication\r\nExcellent English communication skills (written and verbal)\r\nAbility to work independently and manage time effectively in a remote environment\r\nStrong problem-solving and analytical thinking abilities\r\nExperience working with international teams and clients\r\nAdaptability to work across different time zones (availability during US business hours preferred)\r\n\r\n\r\nPreferred QualificationsBonus Skills\r\nExperience with MERN stack (MongoDB, Express, React, Node.js)\r\nKnowledge of TypeScript\r\nFamiliarity with mobile development (React Native, Flutter)\r\nExperience with microservices architecture\r\nKnowledge of GraphQL\r\nUnderstanding of Agile/Scrum methodologies\r\nPrevious experience working with US-based companies or clients\r\n\r\n\r\nCertifications\r\nAWS Certified Developer or similar cloud certifications\r\nRelevant framework certifications (React, Angular, etc.)\r\n\r\n\r\nWhat We OfferCompensation & Benefits\r\nCompetitive salary: NPR 80,000 - NPR 150,000 per month (based on experience and skills)\r\nPerformance-based annual bonuses\r\nHome office setup allowance\r\n\r\n\r\nWork Environment\r\n100% remote work with flexible hours\r\nCollaborative, inclusive team culture\r\nOpportunity to work on diverse, challenging projects\r\nCareer growth opportunities within our expanding organization\r\n\r\n\r\nApplication ProcessHow to Apply\r\nPlease submit the following to careers@techoasisconsulting.com:\r\nUpdated resume/CV highlighting relevant experience\r\nCover letter explaining why you're interested in this role\r\nPortfolio/GitHub profile showcasing your best work\r\n\r\n\r\nEqual Opportunity Employer: We are committed to creating a diverse and inclusive workplace where all qualified applicants receive consideration regardless of race, gender, age, religion, sexual orientation, or disability status.\r\n\r\n\r\nNote: This is a full-time, permanent position with opportunities for long-term career growth within our organization.	{"compatibility_score": 0.32, "compatibility_level": "Poor Match", "detailed_analysis": {"skill_matches": {"Programming": "75%", "Frameworks": "25%", "Cloud": "0%", "Devops": "0%", "Databases": "33%", "Frontend": "28%", "Mobile": "50%", "Security": "0%", "Version_Control": "33%", "Apis": "0%", "Methodologies": "0%"}, "experience_match": "30%", "text_similarity": "9%"}, "recommendations": [{"category": "Programming Skills", "priority": "Medium", "suggestion": "Consider learning typescript", "impact": "Can improve compatibility by 5%"}, {"category": "Frameworks Skills", "priority": "High", "suggestion": "Consider learning django, angular, flutter", "impact": "Can improve compatibility by 30%"}, {"category": "Cloud Skills", "priority": "High", "suggestion": "Consider learning aws, gcp, azure", "impact": "Can improve compatibility by 15%"}, {"category": "Devops Skills", "priority": "High", "suggestion": "Consider learning gitlab, docker", "impact": "Can improve compatibility by 10%"}, {"category": "Databases Skills", "priority": "Medium", "suggestion": "Consider learning mysql, mongodb", "impact": "Can improve compatibility by 10%"}], "improvement_potential": "+25%"}	2025-08-10 04:11:48.043088
2	1	Software Engineer	xyz	0.31	Poor Match	PA WA N B H A T T A R A I\r\nSoftware Engineer\r\nAnamnagar , kathmandu\r\n+9779807990779\r\npawaan012@gmail.com\r\n @ https://www.linkedin.com/in/pawanbhattarai/  @ https://github.com/pawanbhattarai/\r\nPassionate software developer with a focus on customer satisfaction, code quality, and teamwork.\r\nExperienced in spearheading software projects and optimizing processes for e ciency.\r\nEX PER IENCE\r\nSoftware Engineer\r\nM.A.P. Tech Pvt. Ltd.\r\nBhaktapur\r\nJul, 2024 - Present\r\nDeveloped and deployed a Rule-based Chatbot using Python and PostgreSQL capable of processing both Devanagari Nepali and\r\nRomanized Nepali input. This chatbot increased user engagement by 20%.\r\nDesigned and implemented an inventory management system for a small/medium business, improving stock accuracy, cost\r\nsavings.\r\nE ectively troubleshooted and resolved production issues, minimizing downtime and ensuring smooth system operation.\r\nSoftware EngineerKathmandu\r\nPhoenix Solution Pv.Ltd.Jul, 2023 - Jun, 2024\r\nLed development and implementation of Government IMS Software, enhancing administrative e ciency.\r\nContributed to design and implementation of University CRM Software, facilitating departmental collaboration.\r\nLed the development and implementation of a Hospital Management System, incorporating the IMIS\r\nSoftware Developer (Intern)\r\nPhoenix Solution Pv.Ltd.\r\nKathmandu\r\nApr, 2023 - Jul, 2023\r\nCollaborated on Government ERP Software, gathering requirements and ensuring compliance.\r\nAssisted in con guring and customizing ERP system for government regulations.\r\nED UCAT IO N\r\nBachelors in Computer Application\r\nTribhuvan University\r\nKathmandu\r\nOct, 2020 - Present\r\nPR O JECT S\r\nStock Predictor\r\nA web application that predicts NEPSE stock prices for the next 3 to 7 trading days.\r\nTechnologies & Tools: Python, Pandas, NumPy, Flask, Selenium, TensorFlow\r\nAlgorithm: Long Short-Term Memory (LSTM)\r\nLink\r\nJsonToSQL/CSV Converter\r\nA platform where users can input JSON data and convert it into either SQL queries or .CSV les according to their needs.\r\nTechnologies and Tools : Spring Boot, JavaScript, HTML, CSS\r\nLink\r\nS K ILLS\r\nSystem Design, Java, Python, PostgreSQL, SQL, Rest Api, Github, NGINX	About the job\r\nEstablished in 2019, Jaish Global has rapidly evolved into a distinguished solution provider in the cybersecurity space and SI integrator in Digital Transformation using Machine Learning & Artificial Intelligence. Jaish Global Consultancy is an Umbrella company certified by ISO 9001:2015 and ISO 27001. Our unwavering focus on quality and innovative niche technology solutions creates a true edge. Our commitment to excellence has positioned us as a trusted technology-driven organization, safeguarding customer businesses from the ever-evolving landscape of cyber threats and creating business values in customers' enterprise portfolios using our AI tools and services. We never stop pushing the boundaries of what is possible. We are always learning, growing, and re-skilling in Technology solutions and process mapping to stay at the forefront of the industry. Our dynamic culture reflects our drive to be the best. We are providing the services to our customers keeping in view to -> Quick response to change and support for enterprise agility aligned with the business strategy -> Organizational transformation, adopting new trends in business and technology -> Organizational change to support Digital Transformation -> Organizational and operating model changes to improve efficiency and effectiveness -> Lower business operation costs Improved business productivity -> Extending the effective reach of the enterprise (e.g., through digital capability)\r\n\r\nThe Role\r\n\r\nRole Overview\r\n\r\nWe are seeking a skilled and enthusiastic SQL Developer to join our growing data team. In this role, you will be responsible for designing, developing, and maintaining databases and data solutions. The ideal candidate will have a strong understanding of SQL and database principles, with a proven track record of optimizing database performance and ensuring data integrity.\r\n\r\nResponsibilities\r\n\r\nDesign, develop, and implement database solutions, including tables, views, stored procedures, and functions.\r\nWrite complex SQL queries to retrieve, manipulate, and analyze data.\r\nOptimize database performance for speed and efficiency.\r\nEnsure data quality, accuracy, and consistency.\r\nTroubleshoot and resolve database issues.\r\nCollaborate with developers, analysts, and other stakeholders to understand data requirements.\r\nCreate and maintain database documentation.\r\nParticipate in database design and code reviews.\r\nStay up-to-date with the latest SQL Server features and database technologies.\r\nDevelop ETL processes to move data between databases.\r\n\r\nIdeal Profile\r\n\r\nQualifications\r\n\r\nBachelor's degree in Computer Science, Information Systems, or a related field.\r\n2-3 years of experience as a SQL Developer.\r\nStrong proficiency in SQL (e.g., T-SQL, PL/SQL).\r\nExperience with database management systems such as SQL Server, MySQL, or Oracle.\r\nUnderstanding of database design principles and normalization.\r\nExperience with query optimization and performance tuning.\r\nKnowledge of data warehousing concepts.\r\nExcellent analytical and problem-solving skills.\r\nStrong communication and collaboration skills.\r\nAbility to work independently and as part of a team.\r\n\r\nPreferred Skills\r\n\r\nKnowledge of database administration tasks.\r\nFamiliarity with cloud-based database services (e.g., Azure SQL Database, Amazon RDS, Snowflake).\r\nExperience with data visualization tools (e.g., Power BI, Tableau).\r\nKnowledge of scripting languages (e.g., Python, PowerShell).\r\n\r\nWhat's on Offer?\r\n\r\nFantastic work culture	{"compatibility_score": 0.31, "compatibility_level": "Poor Match", "detailed_analysis": {"skill_matches": {"Programming": "100%", "Cloud": "0%", "Databases": "0%", "Data_Science": "0%", "Big_Data": "0%"}, "experience_match": "30%", "text_similarity": "7%"}, "recommendations": [{"category": "Cloud Skills", "priority": "High", "suggestion": "Consider learning azure, rds", "impact": "Can improve compatibility by 10%"}, {"category": "Databases Skills", "priority": "High", "suggestion": "Consider learning oracle, mysql, snowflake", "impact": "Can improve compatibility by 15%"}, {"category": "Data_Science Skills", "priority": "High", "suggestion": "Consider learning tableau", "impact": "Can improve compatibility by 5%"}, {"category": "Big_Data Skills", "priority": "High", "suggestion": "Consider learning snowflake", "impact": "Can improve compatibility by 5%"}, {"category": "Experience", "priority": "High", "suggestion": "Gain more hands-on project experience or consider additional certifications", "impact": "Can improve compatibility by 20%"}], "improvement_potential": "+25%"}	2025-08-10 15:42:39.725218
\.


--
-- Data for Name: email_verifications; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.email_verifications (id, user_id, token, created_at, expires_at, is_used) FROM stdin;
1	1	NiMWrQ1rJiFHhRJZfLG_48qoJDCa9yW4c207INn6bqc	2025-08-10 02:08:53.525532	2025-08-11 02:08:53.523907	f
\.


--
-- Data for Name: password_resets; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.password_resets (id, user_id, token, created_at, expires_at, is_used) FROM stdin;
\.


--
-- Data for Name: saved_resumes; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.saved_resumes (id, user_id, title, content, is_default, created_at, updated_at) FROM stdin;
1	1	Software Engineer	PA WA N B H A T T A R A I\r\nSoftware Engineer\r\nAnamnagar , kathmandu\r\n+9779807990779\r\npawaan012@gmail.com\r\n @ https://www.linkedin.com/in/pawanbhattarai/  @ https://github.com/pawanbhattarai/\r\nPassionate software developer with a focus on customer satisfaction, code quality, and teamwork.\r\nExperienced in spearheading software projects and optimizing processes for e ciency.\r\nEX PER IENCE\r\nSoftware Engineer\r\nM.A.P. Tech Pvt. Ltd.\r\nBhaktapur\r\nJul, 2024 - Present\r\nDeveloped and deployed a Rule-based Chatbot using Python and PostgreSQL capable of processing both Devanagari Nepali and\r\nRomanized Nepali input. This chatbot increased user engagement by 20%.\r\nDesigned and implemented an inventory management system for a small/medium business, improving stock accuracy, cost\r\nsavings.\r\nE ectively troubleshooted and resolved production issues, minimizing downtime and ensuring smooth system operation.\r\nSoftware EngineerKathmandu\r\nPhoenix Solution Pv.Ltd.Jul, 2023 - Jun, 2024\r\nLed development and implementation of Government IMS Software, enhancing administrative e ciency.\r\nContributed to design and implementation of University CRM Software, facilitating departmental collaboration.\r\nLed the development and implementation of a Hospital Management System, incorporating the IMIS\r\nSoftware Developer (Intern)\r\nPhoenix Solution Pv.Ltd.\r\nKathmandu\r\nApr, 2023 - Jul, 2023\r\nCollaborated on Government ERP Software, gathering requirements and ensuring compliance.\r\nAssisted in con guring and customizing ERP system for government regulations.\r\nED UCAT IO N\r\nBachelors in Computer Application\r\nTribhuvan University\r\nKathmandu\r\nOct, 2020 - Present\r\nPR O JECT S\r\nStock Predictor\r\nA web application that predicts NEPSE stock prices for the next 3 to 7 trading days.\r\nTechnologies & Tools: Python, Pandas, NumPy, Flask, Selenium, TensorFlow\r\nAlgorithm: Long Short-Term Memory (LSTM)\r\nLink\r\nJsonToSQL/CSV Converter\r\nA platform where users can input JSON data and convert it into either SQL queries or .CSV les according to their needs.\r\nTechnologies and Tools : Spring Boot, JavaScript, HTML, CSS\r\nLink\r\nS K ILLS\r\nSystem Design, Java, Python, PostgreSQL, SQL, Rest Api, Github, NGINX	t	2025-08-10 04:41:59.260841	2025-08-10 04:41:59.260846
\.


--
-- Data for Name: test_users; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.test_users (id, username, email, password_hash, first_name, last_name, is_verified, created_at, last_login) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.users (id, username, email, password_hash, first_name, last_name, is_verified, created_at, last_login) FROM stdin;
1	pawan	pawankbhattarai67@gmail.com	scrypt:32768:8:1$KfGgyHxiHvdZV2uJ$47aabac9875c4d4e933c625e40a993b91b9c42f6f9adb6eac8b72df884203882ff2b917afee70df6c9b7962a7c5a69b93049504ccbf9b1e15a3c82ae92c73db0	Pawan	Bhattarai	t	2025-08-10 02:08:53.403901	2025-08-10 02:20:46.480558
2	testuser	test@test.com	scrypt:32768:8:1$FHGH7xyqBY5LtKXA$8a1c2b8f2e59b2e4a9d0c8e1f3a5b7c9d2e6f8a1c4b7e0f3a6c9d2e5f8b1c4a7e0f3b6c9d2e5f8a1c4b7e0f3a6	Test	User	t	2025-08-10 02:20:48.004673	\N
3	testuser123	test123@example.com	scrypt:32768:8:1$salt123$hashedpassword	Test	User	t	2025-08-10 04:13:31.49569	\N
\.


--
-- Name: analysis_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.analysis_history_id_seq', 2, true);


--
-- Name: email_verifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.email_verifications_id_seq', 1, true);


--
-- Name: password_resets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.password_resets_id_seq', 1, false);


--
-- Name: saved_resumes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.saved_resumes_id_seq', 1, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


--
-- Name: analysis_history analysis_history_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.analysis_history
    ADD CONSTRAINT analysis_history_pkey PRIMARY KEY (id);


--
-- Name: email_verifications email_verifications_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.email_verifications
    ADD CONSTRAINT email_verifications_pkey PRIMARY KEY (id);


--
-- Name: email_verifications email_verifications_token_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.email_verifications
    ADD CONSTRAINT email_verifications_token_key UNIQUE (token);


--
-- Name: password_resets password_resets_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.password_resets
    ADD CONSTRAINT password_resets_pkey PRIMARY KEY (id);


--
-- Name: password_resets password_resets_token_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.password_resets
    ADD CONSTRAINT password_resets_token_key UNIQUE (token);


--
-- Name: saved_resumes saved_resumes_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.saved_resumes
    ADD CONSTRAINT saved_resumes_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: analysis_history analysis_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.analysis_history
    ADD CONSTRAINT analysis_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: email_verifications email_verifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.email_verifications
    ADD CONSTRAINT email_verifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: password_resets password_resets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.password_resets
    ADD CONSTRAINT password_resets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: saved_resumes saved_resumes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.saved_resumes
    ADD CONSTRAINT saved_resumes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO neon_superuser WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLES TO neon_superuser WITH GRANT OPTION;


--
-- PostgreSQL database dump complete
--

