--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

-- Started on 2025-06-06 14:53:31

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- TOC entry 219 (class 1259 OID 66238)
-- Name: directions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.directions (
    id integer NOT NULL,
    code character varying(8) NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.directions OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 66237)
-- Name: directions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.directions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.directions_id_seq OWNER TO postgres;

--
-- TOC entry 4948 (class 0 OID 0)
-- Dependencies: 218
-- Name: directions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.directions_id_seq OWNED BY public.directions.id;


--
-- TOC entry 223 (class 1259 OID 66260)
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    id integer NOT NULL,
    login text NOT NULL,
    password text NOT NULL
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 66259)
-- Name: employees_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employees_id_seq OWNER TO postgres;

--
-- TOC entry 4949 (class 0 OID 0)
-- Dependencies: 222
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- TOC entry 217 (class 1259 OID 66227)
-- Name: support_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.support_categories (
    id integer NOT NULL,
    name text NOT NULL,
    semester_payment integer NOT NULL
);


ALTER TABLE public.support_categories OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 66226)
-- Name: financial_situations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.financial_situations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.financial_situations_id_seq OWNER TO postgres;

--
-- TOC entry 4950 (class 0 OID 0)
-- Dependencies: 216
-- Name: financial_situations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.financial_situations_id_seq OWNED BY public.support_categories.id;


--
-- TOC entry 232 (class 1259 OID 66392)
-- Name: grades; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.grades (
    student_id integer NOT NULL,
    subject_id integer NOT NULL,
    grade integer NOT NULL,
    CONSTRAINT grades_grade_check CHECK (((grade = 2) OR (grade = 3) OR (grade = 4) OR (grade = 5)))
);


ALTER TABLE public.grades OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 66251)
-- Name: groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.groups (
    id integer NOT NULL,
    name character varying(15) NOT NULL
);


ALTER TABLE public.groups OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 66250)
-- Name: groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.groups_id_seq OWNER TO postgres;

--
-- TOC entry 4951 (class 0 OID 0)
-- Dependencies: 220
-- Name: groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.groups_id_seq OWNED BY public.groups.id;


--
-- TOC entry 229 (class 1259 OID 66356)
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    number integer NOT NULL,
    date date DEFAULT CURRENT_DATE NOT NULL,
    scope character varying(9) NOT NULL,
    institute_number integer,
    group_id integer,
    student_id integer,
    enrollment_amount integer NOT NULL,
    CONSTRAINT orders_check CHECK ((num_nonnulls(institute_number, group_id, student_id) = 1)),
    CONSTRAINT orders_scope_check CHECK ((((scope)::text = 'institute'::text) OR ((scope)::text = 'group'::text) OR ((scope)::text = 'student'::text)))
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 66355)
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_id_seq OWNER TO postgres;

--
-- TOC entry 4952 (class 0 OID 0)
-- Dependencies: 228
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- TOC entry 226 (class 1259 OID 66333)
-- Name: payment_methods; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payment_methods (
    student_id integer NOT NULL,
    type character varying(15) NOT NULL,
    bank text,
    phone_number character varying(11),
    payment_account character varying(20),
    CONSTRAINT payment_methods_type_check CHECK ((((type)::text = 'in_cash'::text) OR ((type)::text = 'bank_card'::text) OR ((type)::text = 'payment_account'::text)))
);


ALTER TABLE public.payment_methods OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 66344)
-- Name: penalties; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.penalties (
    student_id integer NOT NULL,
    name text NOT NULL,
    amount integer NOT NULL
);


ALTER TABLE public.penalties OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 66308)
-- Name: students; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.students (
    id integer NOT NULL,
    surname text NOT NULL,
    name text NOT NULL,
    patronymic text NOT NULL,
    passport_serie character varying(4) NOT NULL,
    passport_number character varying(6) NOT NULL,
    address text NOT NULL,
    institute_number integer NOT NULL,
    group_id integer NOT NULL,
    course integer NOT NULL,
    direction_id integer NOT NULL,
    no_scholarship_reason text,
    is_trade_union_member boolean NOT NULL,
    support_category_id integer NOT NULL
);


ALTER TABLE public.students OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 66307)
-- Name: students_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.students_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.students_id_seq OWNER TO postgres;

--
-- TOC entry 4953 (class 0 OID 0)
-- Dependencies: 224
-- Name: students_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.students_id_seq OWNED BY public.students.id;


--
-- TOC entry 231 (class 1259 OID 66382)
-- Name: subjects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subjects (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.subjects OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 66381)
-- Name: subjects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subjects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subjects_id_seq OWNER TO postgres;

--
-- TOC entry 4954 (class 0 OID 0)
-- Dependencies: 230
-- Name: subjects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subjects_id_seq OWNED BY public.subjects.id;


--
-- TOC entry 4731 (class 2604 OID 66241)
-- Name: directions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.directions ALTER COLUMN id SET DEFAULT nextval('public.directions_id_seq'::regclass);


--
-- TOC entry 4733 (class 2604 OID 66263)
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- TOC entry 4732 (class 2604 OID 66254)
-- Name: groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups ALTER COLUMN id SET DEFAULT nextval('public.groups_id_seq'::regclass);


--
-- TOC entry 4735 (class 2604 OID 66359)
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- TOC entry 4734 (class 2604 OID 66311)
-- Name: students id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students ALTER COLUMN id SET DEFAULT nextval('public.students_id_seq'::regclass);


--
-- TOC entry 4737 (class 2604 OID 66385)
-- Name: subjects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects ALTER COLUMN id SET DEFAULT nextval('public.subjects_id_seq'::regclass);


--
-- TOC entry 4730 (class 2604 OID 66230)
-- Name: support_categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.support_categories ALTER COLUMN id SET DEFAULT nextval('public.financial_situations_id_seq'::regclass);


--
-- TOC entry 4929 (class 0 OID 66238)
-- Dependencies: 219
-- Data for Name: directions; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.directions VALUES (1, '01.03.02', 'Компьютерные науки и прикладная математика');
INSERT INTO public.directions VALUES (4, '01.03.04', 'Компьютерные науки и прикладная математика');
INSERT INTO public.directions VALUES (5, '02.03.02', 'Фундаментальная информатика и информационные технологии');
INSERT INTO public.directions VALUES (6, '05.03.06', 'Экология и природопользование');
INSERT INTO public.directions VALUES (7, '09.03.01', 'Информатика и вычислительная техника');
INSERT INTO public.directions VALUES (8, '09.03.02', 'Информационные системы и технологии');
INSERT INTO public.directions VALUES (9, '09.03.03', 'Прикладная информатика');
INSERT INTO public.directions VALUES (10, '09.03.04', 'Программная инженерия');
INSERT INTO public.directions VALUES (11, '12.03.04', 'Биотехнические системы и технологии');
INSERT INTO public.directions VALUES (12, '13.03.01', 'Теплоэнергетика и теплотехника');
INSERT INTO public.directions VALUES (13, '13.03.02', 'Электроэнергетика и электротехника');
INSERT INTO public.directions VALUES (14, '22.03.01', 'Новые материалы и цифровые технологии');
INSERT INTO public.directions VALUES (15, '22.03.02', 'Новые материалы и цифровые технологии');
INSERT INTO public.directions VALUES (16, '24.03.04', 'Авиастроение');
INSERT INTO public.directions VALUES (17, '25.03.01', 'Техническая эксплуатация летательных аппаратов');
INSERT INTO public.directions VALUES (18, '27.03.03', 'Системный анализ и управление');
INSERT INTO public.directions VALUES (19, '27.03.04', 'Управление в технических системах');
INSERT INTO public.directions VALUES (20, '27.03.05', 'Инноватика');
INSERT INTO public.directions VALUES (21, '38.03.01', 'Экономика и управление');
INSERT INTO public.directions VALUES (22, '38.03.02', 'Экономика и управление');
INSERT INTO public.directions VALUES (23, '38.03.03', 'Управление персоналом');
INSERT INTO public.directions VALUES (24, '38.03.04', 'Государственное и муниципальное управление');
INSERT INTO public.directions VALUES (25, '38.03.05', 'Бизнес-информатика');
INSERT INTO public.directions VALUES (26, '42.03.01', 'Реклама и связи с общественностью');
INSERT INTO public.directions VALUES (27, '45.03.02', 'Лингвистика');
INSERT INTO public.directions VALUES (28, '10.05.02', 'Информационная безопасность телекоммуникационных систем');
INSERT INTO public.directions VALUES (29, '11.05.01', 'Радиоэлектронные системы и комплексы');
INSERT INTO public.directions VALUES (30, '24.05.01', 'Проектирование, производство и эксплуатация ракет и ракетно-космических комплексов');
INSERT INTO public.directions VALUES (31, '24.05.02', 'Проектирование авиационных и ракетных двигателей');
INSERT INTO public.directions VALUES (32, '24.05.05', 'Интегрирование системы летательных аппаратов');
INSERT INTO public.directions VALUES (33, '24.05.06', 'Системы управления летательных аппаратов');
INSERT INTO public.directions VALUES (34, '24.05.07', 'Самолето- и вертолетостроение');
INSERT INTO public.directions VALUES (35, '27.05.01', 'Специальные организационно-технические системы');


--
-- TOC entry 4933 (class 0 OID 66260)
-- Dependencies: 223
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.employees VALUES (1, 'root', '$1$GZ2kOlmf$KuEAHbcBNxwD32ORMzaJZ/');


--
-- TOC entry 4942 (class 0 OID 66392)
-- Dependencies: 232
-- Data for Name: grades; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.grades VALUES (4, 14, 5);
INSERT INTO public.grades VALUES (3, 14, 5);


--
-- TOC entry 4931 (class 0 OID 66251)
-- Dependencies: 221
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.groups VALUES (4, 'М3О-314Б-21');


--
-- TOC entry 4939 (class 0 OID 66356)
-- Dependencies: 229
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 4936 (class 0 OID 66333)
-- Dependencies: 226
-- Data for Name: payment_methods; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.payment_methods VALUES (3, 'payment_account', '', '', '12345678901234567890');
INSERT INTO public.payment_methods VALUES (4, 'bank_card', 'СДМ', '88005553535', '');


--
-- TOC entry 4937 (class 0 OID 66344)
-- Dependencies: 227
-- Data for Name: penalties; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.penalties VALUES (3, 'накричал на себя', 50000);


--
-- TOC entry 4935 (class 0 OID 66308)
-- Dependencies: 225
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.students VALUES (3, 'Иванов', 'Иван', 'Иванович', '1234', '567890', 'г. Москва, Волоколамское ш., д.4, кв. 3', 3, 4, 3, 8, NULL, true, 11);
INSERT INTO public.students VALUES (4, 'Подосенова', 'Анна', 'Александровна', '1111', '222222', 'г.Москва, ул. Садовая-Кудринская, 14-16', 3, 4, 3, 8, NULL, true, 1);


--
-- TOC entry 4941 (class 0 OID 66382)
-- Dependencies: 231
-- Data for Name: subjects; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.subjects VALUES (14, 'Основы теории управления');


--
-- TOC entry 4927 (class 0 OID 66227)
-- Dependencies: 217
-- Data for Name: support_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.support_categories VALUES (3, 'Сирота', 40000);
INSERT INTO public.support_categories VALUES (4, 'Инвалид', 50000);
INSERT INTO public.support_categories VALUES (5, 'Участник военных действий', 30000);
INSERT INTO public.support_categories VALUES (6, 'Есть ребенок', 35000);
INSERT INTO public.support_categories VALUES (7, 'Чернобылец', 18000);
INSERT INTO public.support_categories VALUES (8, 'Из многодетной семьи', 13000);
INSERT INTO public.support_categories VALUES (9, 'Оба родителя инвалиды или пенсионеры', 33000);
INSERT INTO public.support_categories VALUES (10, 'Неполная семья', 17000);
INSERT INTO public.support_categories VALUES (11, 'Проживает в общежитии', 39000);
INSERT INTO public.support_categories VALUES (12, 'Хроническое заболевание', 11000);
INSERT INTO public.support_categories VALUES (1, 'Нет', 0);


--
-- TOC entry 4955 (class 0 OID 0)
-- Dependencies: 218
-- Name: directions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.directions_id_seq', 35, true);


--
-- TOC entry 4956 (class 0 OID 0)
-- Dependencies: 222
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_id_seq', 8, true);


--
-- TOC entry 4957 (class 0 OID 0)
-- Dependencies: 216
-- Name: financial_situations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.financial_situations_id_seq', 12, true);


--
-- TOC entry 4958 (class 0 OID 0)
-- Dependencies: 220
-- Name: groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.groups_id_seq', 4, true);


--
-- TOC entry 4959 (class 0 OID 0)
-- Dependencies: 228
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 9, true);


--
-- TOC entry 4960 (class 0 OID 0)
-- Dependencies: 224
-- Name: students_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.students_id_seq', 4, true);


--
-- TOC entry 4961 (class 0 OID 0)
-- Dependencies: 230
-- Name: subjects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subjects_id_seq', 14, true);


--
-- TOC entry 4747 (class 2606 OID 66247)
-- Name: directions directions_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.directions
    ADD CONSTRAINT directions_code_key UNIQUE (code);


--
-- TOC entry 4749 (class 2606 OID 66245)
-- Name: directions directions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.directions
    ADD CONSTRAINT directions_pkey PRIMARY KEY (id);


--
-- TOC entry 4755 (class 2606 OID 66269)
-- Name: employees employees_login_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_login_key UNIQUE (login);


--
-- TOC entry 4757 (class 2606 OID 66267)
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- TOC entry 4773 (class 2606 OID 74385)
-- Name: grades grades_student_id_subject_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades
    ADD CONSTRAINT grades_student_id_subject_id_key UNIQUE (student_id, subject_id);


--
-- TOC entry 4751 (class 2606 OID 66258)
-- Name: groups groups_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_name_key UNIQUE (name);


--
-- TOC entry 4753 (class 2606 OID 66256)
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- TOC entry 4765 (class 2606 OID 66364)
-- Name: orders orders_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_number_key UNIQUE (number);


--
-- TOC entry 4767 (class 2606 OID 66362)
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- TOC entry 4763 (class 2606 OID 74383)
-- Name: payment_methods payment_methods_student_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_methods
    ADD CONSTRAINT payment_methods_student_id_key UNIQUE (student_id);


--
-- TOC entry 4759 (class 2606 OID 66332)
-- Name: students students_passport_serie_passport_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_passport_serie_passport_number_key UNIQUE (passport_serie, passport_number);


--
-- TOC entry 4761 (class 2606 OID 66315)
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (id);


--
-- TOC entry 4769 (class 2606 OID 66391)
-- Name: subjects subjects_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_name_key UNIQUE (name);


--
-- TOC entry 4771 (class 2606 OID 66389)
-- Name: subjects subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_pkey PRIMARY KEY (id);


--
-- TOC entry 4743 (class 2606 OID 66236)
-- Name: support_categories support_categories_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.support_categories
    ADD CONSTRAINT support_categories_name_key UNIQUE (name);


--
-- TOC entry 4745 (class 2606 OID 66234)
-- Name: support_categories support_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.support_categories
    ADD CONSTRAINT support_categories_pkey PRIMARY KEY (id);


--
-- TOC entry 4781 (class 2606 OID 66396)
-- Name: grades grades_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades
    ADD CONSTRAINT grades_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id);


--
-- TOC entry 4782 (class 2606 OID 66401)
-- Name: grades grades_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades
    ADD CONSTRAINT grades_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES public.subjects(id);


--
-- TOC entry 4779 (class 2606 OID 66365)
-- Name: orders orders_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id);


--
-- TOC entry 4780 (class 2606 OID 66370)
-- Name: orders orders_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id);


--
-- TOC entry 4777 (class 2606 OID 66339)
-- Name: payment_methods payment_methods_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_methods
    ADD CONSTRAINT payment_methods_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id);


--
-- TOC entry 4778 (class 2606 OID 66350)
-- Name: penalties penalties_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.penalties
    ADD CONSTRAINT penalties_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id);


--
-- TOC entry 4774 (class 2606 OID 66321)
-- Name: students students_direction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_direction_id_fkey FOREIGN KEY (direction_id) REFERENCES public.directions(id);


--
-- TOC entry 4775 (class 2606 OID 66316)
-- Name: students students_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id);


--
-- TOC entry 4776 (class 2606 OID 66376)
-- Name: students students_support_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_support_category_id_fkey FOREIGN KEY (support_category_id) REFERENCES public.support_categories(id);


-- Completed on 2025-06-06 14:53:32

--
-- PostgreSQL database dump complete
--

