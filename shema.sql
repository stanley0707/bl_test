--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1
-- Dumped by pg_dump version 14.1

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
-- Name: Account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Account" (
    time_created timestamp with time zone DEFAULT now(),
    time_updated timestamp with time zone,
    work_timing json,
    id integer NOT NULL,
    first_name character varying,
    last_name character varying,
    email character varying,
    password character varying NOT NULL,
    role character varying DEFAULT 'admin'::character varying NOT NULL
);


ALTER TABLE public."Account" OWNER TO postgres;

--
-- Name: Account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Account_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Account_id_seq" OWNER TO postgres;

--
-- Name: Account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Account_id_seq" OWNED BY public."Account".id;


--
-- Name: Event; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Event" (
    time_created timestamp with time zone DEFAULT now(),
    time_updated timestamp with time zone,
    id integer NOT NULL,
    author_id integer NOT NULL,
    title character varying NOT NULL,
    description character varying,
    meeting_url character varying,
    time_start timestamp with time zone DEFAULT now(),
    time_end timestamp with time zone DEFAULT now()
);


ALTER TABLE public."Event" OWNER TO postgres;

--
-- Name: EventAccountInvite; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."EventAccountInvite" (
    time_created timestamp with time zone DEFAULT now(),
    time_updated timestamp with time zone,
    id integer NOT NULL,
    event_id integer NOT NULL,
    guest_id integer NOT NULL,
    is_confirmed boolean
);


ALTER TABLE public."EventAccountInvite" OWNER TO postgres;

--
-- Name: EventAccountInvite_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."EventAccountInvite_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."EventAccountInvite_id_seq" OWNER TO postgres;

--
-- Name: EventAccountInvite_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."EventAccountInvite_id_seq" OWNED BY public."EventAccountInvite".id;


--
-- Name: Event_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Event_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Event_id_seq" OWNER TO postgres;

--
-- Name: Event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Event_id_seq" OWNED BY public."Event".id;


--
-- Name: Invite; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Invite" (
    time_created timestamp with time zone DEFAULT now(),
    time_updated timestamp with time zone,
    id integer NOT NULL,
    inviter_id integer NOT NULL,
    invite_id integer NOT NULL,
    is_confirmed boolean
);


ALTER TABLE public."Invite" OWNER TO postgres;

--
-- Name: Invite_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Invite_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Invite_id_seq" OWNER TO postgres;

--
-- Name: Invite_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Invite_id_seq" OWNED BY public."Invite".id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: Account id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Account" ALTER COLUMN id SET DEFAULT nextval('public."Account_id_seq"'::regclass);


--
-- Name: Event id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event" ALTER COLUMN id SET DEFAULT nextval('public."Event_id_seq"'::regclass);


--
-- Name: EventAccountInvite id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventAccountInvite" ALTER COLUMN id SET DEFAULT nextval('public."EventAccountInvite_id_seq"'::regclass);


--
-- Name: Invite id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Invite" ALTER COLUMN id SET DEFAULT nextval('public."Invite_id_seq"'::regclass);


--
-- Data for Name: Account; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Account" (time_created, time_updated, work_timing, id, first_name, last_name, email, password, role) FROM stdin;
2023-02-06 20:07:31.36642+00	\N	"{\\"Monday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Tuesday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Wednesday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Thursday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Friday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Saturday\\": null, \\"Sunday\\": null}"	1	\N	\N	user@example.com	$2b$12$CGif/olFZteDzeFo4ZVkZ.ii5qyxkEC.JUMCj..olcdmoF7bbe7ZS	user
2023-02-06 20:07:37.024117+00	\N	"{\\"Monday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Tuesday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Wednesday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Thursday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Friday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Saturday\\": null, \\"Sunday\\": null}"	2	\N	\N	user2@example.com	$2b$12$KMzoCXX.9uYfnt8g6SWA/eXkh3h9XwJdqcfQf2anhrS/TjPWpWfMy	user
2023-02-06 20:07:40.735817+00	\N	"{\\"Monday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Tuesday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Wednesday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Thursday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Friday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Saturday\\": null, \\"Sunday\\": null}"	3	\N	\N	user3@example.com	$2b$12$kFWPGmdSGnc7YqCnsuRXyu5o1l3Cs7BgpWHPpmqL1ZI26CmIBXbhS	user
2023-02-06 20:07:45.897713+00	\N	"{\\"Monday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Tuesday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Wednesday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Thursday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Friday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Saturday\\": null, \\"Sunday\\": null}"	4	\N	\N	user4@example.com	$2b$12$xkyqplkBNqamUrr3FxNJueT8it4We0rVDM/9qnQtA4Vl8.Uim/hXe	user
2023-02-07 13:27:22.438829+00	\N	"{\\"Monday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Tuesday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Wednesday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Thursday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Friday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Saturday\\": null, \\"Sunday\\": null}"	5	\N	\N	user10@example.com	$2b$12$xiifG.ArvGHug4W2yjHVt.Nw4bBqPtbm8KzpbzCntRmTmp/Imy.qK	user
2023-02-07 14:32:21.009124+00	\N	"{\\"Monday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Tuesday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Wednesday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Thursday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Friday\\": {\\"start\\": \\"10:00:00\\", \\"end\\": \\"18:00:00\\", \\"break_start\\": \\"12:00:00\\", \\"break_end\\": \\"13:00:00\\"}, \\"Saturday\\": null, \\"Sunday\\": null}"	6	\N	\N	user11@example.com	$2b$12$yBg38OAbfDgoLl./1cw0eejIvVPjJQZC6FuQAXNnUsM4Tc2wxOHn6	user
\.


--
-- Data for Name: Event; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Event" (time_created, time_updated, id, author_id, title, description, meeting_url, time_start, time_end) FROM stdin;
2023-02-06 12:00:00+00	2023-02-06 20:09:41.610584+00	1	1	Встреча номер один	Самая важная встреча в мире!	какой-то урл	2023-02-07 12:00:00+00	2023-02-07 13:00:00+00
2023-02-07 12:00:00+00	2023-02-07 10:57:26+00	2	3	Второе событие	Второе не менее важное событие	какой-то второй урд	2023-02-15 15:00:00+00	2023-02-15 16:20:00+00
\.


--
-- Data for Name: EventAccountInvite; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."EventAccountInvite" (time_created, time_updated, id, event_id, guest_id, is_confirmed) FROM stdin;
2023-02-06 20:09:41.610584+00	\N	1	1	1	f
2023-02-07 10:57:26.785793+00	\N	5	2	4	f
2023-02-07 10:57:26+00	2023-02-07 12:31:36.730064+00	4	2	3	t
2023-02-07 12:38:53.802396+00	\N	6	2	2	f
2023-02-07 14:15:49.964978+00	\N	7	1	5	t
2023-02-07 14:35:44.773173+00	\N	8	1	6	t
\.


--
-- Data for Name: Invite; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Invite" (time_created, time_updated, id, inviter_id, invite_id, is_confirmed) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
900fa3141351
\.


--
-- Name: Account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Account_id_seq"', 6, true);


--
-- Name: EventAccountInvite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."EventAccountInvite_id_seq"', 8, true);


--
-- Name: Event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Event_id_seq"', 2, true);


--
-- Name: Invite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Invite_id_seq"', 1, false);


--
-- Name: Account Account_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Account"
    ADD CONSTRAINT "Account_email_key" UNIQUE (email);


--
-- Name: Account Account_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Account"
    ADD CONSTRAINT "Account_pkey" PRIMARY KEY (id);


--
-- Name: EventAccountInvite EventAccountInvite_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventAccountInvite"
    ADD CONSTRAINT "EventAccountInvite_pkey" PRIMARY KEY (id);


--
-- Name: Event Event_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event"
    ADD CONSTRAINT "Event_pkey" PRIMARY KEY (id);


--
-- Name: Invite Invite_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Invite"
    ADD CONSTRAINT "Invite_pkey" PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: EventAccountInvite EventAccountInvite_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventAccountInvite"
    ADD CONSTRAINT "EventAccountInvite_event_id_fkey" FOREIGN KEY (event_id) REFERENCES public."Event"(id) ON DELETE CASCADE;


--
-- Name: EventAccountInvite EventAccountInvite_guest_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventAccountInvite"
    ADD CONSTRAINT "EventAccountInvite_guest_id_fkey" FOREIGN KEY (guest_id) REFERENCES public."Account"(id) ON DELETE SET NULL;


--
-- Name: Event Event_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event"
    ADD CONSTRAINT "Event_author_id_fkey" FOREIGN KEY (author_id) REFERENCES public."Account"(id) ON DELETE SET NULL;


--
-- Name: Invite Invite_invite_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Invite"
    ADD CONSTRAINT "Invite_invite_id_fkey" FOREIGN KEY (invite_id) REFERENCES public."EventAccountInvite"(id) ON DELETE CASCADE;


--
-- Name: Invite Invite_inviter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Invite"
    ADD CONSTRAINT "Invite_inviter_id_fkey" FOREIGN KEY (inviter_id) REFERENCES public."Account"(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

