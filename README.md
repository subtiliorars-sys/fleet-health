# Fleet Health Dashboard

<p align="center">
  <img src="assets/dashboard-preview.png" alt="Fleet Health Dashboard" width="600">
</p>

<p align="center">
  <strong>Single-pane status dashboard for all your services, PRs, and issues.</strong>
</p>

<p align="center">
  <a href="https://omnitender.gumroad.com/l/ixrsyx?discount=LAUNCH50"><img src="https://img.shields.io/badge/Get_the_Field_Guide-50%25_OFF-orange" alt="Get the Field Guide"></a>
  <a href="https://github.com/subtiliorars-sys/fleet-health"><img src="https://img.shields.io/badge/Star_on_GitHub-⭐_Stars-blue" alt="Star on GitHub"></a>
</p>

---

## 🚨 The Problem

You're managing multiple services, PRs, and kanban boards across different repos. Right now you're probably:

- Tab-switching between 10+ dashboards
- Manually checking service health
- Missing PRs that need attention
- No single view of your entire operation

**There's a better way.**

---

## ✨ What Is Fleet Health?

Fleet Health is a **single-page status dashboard** that aggregates all your subtiliorars-sys services, pull requests, and kanban issues into one clean, real-time view.

### Features

- 📊 **Service Status** — See health of all your services at a glance
- 🔄 **PR Tracking** — Monitor open pull requests across repos
- 📋 **Kanban Integration** — View issues and project progress
- 🚀 **One-Click Deploy** — Deploy to Fly.io in seconds
- 📱 **Responsive Design** — Works on desktop and mobile
- ⚡ **Real-time Updates** — Always current, no refresh needed

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Installation

```bash
# Clone the repo
git clone https://github.com/subtiliorars-sys/fleet-health.git
cd fleet-health

# Install dependencies
uv sync

# Run the server
uv run uvicorn main:app --reload --port 8091
```

Visit `http://localhost:8091` to see your dashboard.

---

## 🛠️ Deployment

### Deploy to Fly.io

```bash
# Launch (first time)
fly launch

# Deploy updates
fly deploy
```

See [fly.toml](fly.toml) for configuration.

---

## 📚 Companion Guide

**Want to scale beyond one dashboard?** Check out:

> **[Running a Multi-Agent AI Coding Fleet: A Field Guide](https://omnitender.gumroad.com/l/ixrsyx?discount=LAUNCH50)**
>
> Learn how to coordinate 70+ repos with AI agents, prevent token waste, and automate your entire workflow.
>
> **Use code `LAUNCH50` for 50% off** (first 10 customers only)

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🌟 Support

If this project helps you, please consider:

- ⭐ **Starring the repo** — helps others find it
- 🐦 **Sharing on Twitter** — spread the word
- 💬 **Joining the discussion** — open an issue or PR

<p align="center">
  <strong>Built with ❤️ for the AI-native development community</strong>
</p>
