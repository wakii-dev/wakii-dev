<div align="center">
  <img src="assets/hero.svg" width="100%" alt="Wakii × HoiVu" />

  <a href="https://wakii.dev">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1200&color=C026D3&center=true&vCenter=true&random=false&width=520&lines=Building+Wakii+%E2%9A%A1+agentic+IDE;A+team+of+agents%2C+built+in.;Human+%C3%97+AI+agents%2C+one+flow." alt="Typing SVG" />
  </a>

  🌐 <a href="https://wakii.dev"><b>wakii.dev</b></a> · <a href="https://github.com/wakii-dev/wakii-site">wakii-site</a> · <a href="https://github.com/wakii-dev/hub-store">hub-store</a>
</div>

---

## 🖥️ How I ship

| <img src="assets/terminal.svg" width="560" alt="wakii up terminal" /> | **Human × AI agents** — specs and judgment from me, execution at agent speed (Claude, Kiro).<br /><br />Every project here — including the 2.5M-order logistics platform — was built in this loop: **spec → plan → parallel agents → review → ship.** |
| -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

## 🤖 The agent crew (my contributors)

<div align="center">
  <img src="assets/agents.svg" width="100%" alt="Wakii agent crew: spec-critic, impact-analyst, plan-critic, task-executor, code-reviewer, verifier, security-audit, rollback-fixer, designer" />
</div>

*9 agents ship with every Wakii install. The site, the IDE docs, this profile
and the 2.5M-order platform below were all spec'd, built and reviewed by this
crew — the profile is the demo.*

## ⚙️ The pipeline

<div align="center">
  <img src="assets/pipeline.svg" width="100%" alt="idea → impact → plan → bracket → parallel SFs → gates → PR" />
</div>

## 🚀 What I'm building

### ⚡ [Wakii](https://wakii.dev) — agentic IDE (ADE)
> The desktop for working with a **fleet of parallel coding agents** — run any
> coding agent with your own subscription. Available on desktop, mobile & VPS.

- Core: [`wakii`](https://github.com/wakii-dev/wakii) (TypeScript) · site: [wakii.dev](https://wakii.dev) → [`wakii-site`](https://github.com/wakii-dev/wakii-site) (Astro)
- Docs, skills catalog (20 built-in skills), public roadmap & downloads

### 🏗️ hub-store — fulfillment operations platform *(private — architecture below)*
> Production-grade logistics platform exercised at **2.5M+ orders / year scale**:
> order coordination, warehouse picking batches, D2C carrier hand-off,
> technician dispatch, COD settlement, label printing.

```mermaid
graph LR
    MFE["React 18 microfrontends<br/>Module Federation"] --> BFF["Fastify BFF"]
    BFF -->|gRPC| ORD["order-svc<br/>Java 17 · Spring Boot"]
    BFF -->|gRPC| WHS["warehouse-svc<br/>Go"]
    BFF -->|gRPC| CAR["carrier-svc<br/>Python"]
    ORD --> PG1[("PostgreSQL")]
    WHS --> PG2[("PostgreSQL")]
    ORD -.->|events| K["Kafka"]
    WHS -.->|events| K
    SSO["Keycloak OIDC"] --> BFF
```

- Polyglot microservices over **gRPC** · PostgreSQL dual-DB · Kafka side-channel
- **Full QA story**: role-matrix regression suites, Playwright e2e, CI on Actions

### 🎯 wakii-english — AI IELTS prep for Vietnamese learners *(private — architecture below)*
> AI scores Writing/Speaking to **≤ 0.5 band accuracy**, builds a personalized
> roadmap, runs a multi-tenant LMS.

```mermaid
graph LR
    APP["Next.js + Vite<br/>learning apps"] --> API["Spring Boot 3<br/>microservices"]
    API --> PG[("PostgreSQL<br/>RLS multi-tenant")]
    API <--> K["Kafka"]
    AI["AI grading<br/>Writing / Speaking"] --- API
    OPS["Keycloak · observability<br/>wakii-infra"] --- API
```

### 🧪 More builds
- 🎧 [`iloveenglishclub`](https://github.com/wakii-dev/iloveenglishclub) — English listening
  dictation practice following the Cambridge Prepare path (Pre-A1 → B2 First)
  · Next.js 15 + Drizzle + Auth.js + Neon Postgres
- 🛒 [`ecommerce`](https://github.com/wakii-dev/ecommerce) — Spring Boot 3 microservices +
  React/Vite microfrontends (Module Federation), Tiki-inspired storefront
  · PostgreSQL · Redis · RabbitMQ · MongoDB · Elasticsearch · Stripe
- 🔌 `cc-driver` *(private)* — TypeScript driver to orchestrate Claude Code headless
  (agents, pools, goal/loop, background jobs) + schema-validated LLM calls
  · GLM (z.ai) / Claude multi-provider, zero runtime deps

## 🧰 Stack I work with

![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![Astro](https://img.shields.io/badge/Astro-BC52EE?style=flat-square&logo=astro&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![gRPC](https://img.shields.io/badge/gRPC-244B5A?style=flat-square&logo=googlechrome&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Kafka](https://img.shields.io/badge/Kafka-231F20?style=flat-square&logo=apachekafka&logoColor=white)
![Keycloak](https://img.shields.io/badge/Keycloak-008AAA?style=flat-square&logo=keycloak&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)

## 📊 Mission control

<div align="center">
  <img src="assets/mission-control.svg?v=1793005914" width="100%" alt="mission control stats" />
</div>

## 🧊 Contributions in 3D

<div align="center">
  <img src="profile-3d-contrib/profile-green-animate.svg?v=1793005914" width="100%" alt="3D contribution graph" />
</div>

## 🐍 Snake

<p align="center">
  <img alt="contribution snake" src="https://raw.githubusercontent.com/wakii-dev/wakii-dev/output/github-snake.svg" />
</p>

---

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:DB2777,50:C026D3,100:6D28D9&height=110&section=footer&animation=fadeIn" width="100%" />
</div>

<div align="center"><i>Building in public, one agent-crew sprint at a time. 🤖</i></div>
