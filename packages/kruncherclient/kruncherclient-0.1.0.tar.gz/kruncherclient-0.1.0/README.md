# Kruncher Client

![Kruncher Logo](https://kruncher.ai/images/brand/header-logo.svg)

Kruncher Client is a Python library for interacting with [Kruncher](https://kruncher.ai) data, allowing users to seamlessly access and analyze structured information.

## 🚀 Installation

To install the `kruncher-client` library, use pip:

```bash
pip install kruncher-client
```

<!-- Alternatively, install dependencies directly from `requirements.txt`:

```bash
pip install -r requirements.txt
``` -->

---

## 🔑 API Key Setup

To use the Kruncher API, an API key is required. Follow these steps to obtain it:

1. Log in to your account on [kruncher.ai](https://kruncher.ai) with an **owner/admin** account.
2. Navigate to **Settings**.
3. Go to **Integrations**.
4. Copy the `KRUNCHER_API_KEY` and store it securely.

Save it in a `.env` file within your project directory:

```ini
KRUNCHER_API_KEY=your_api_key_here
```

Or set it as an environment variable:

```bash
export KRUNCHER_API_KEY=your_api_key_here
```

---

## 📖 Usage

To use the `KruncherClient`, either pass the API key directly when initializing the client or ensure it is set in your environment variables.

### ✅ Basic Example

```python
from kruncher import KruncherClient

# Initialize the client with the API key
client = KruncherClient(api_key='your_api_key_here')

# Alternatively, if the API key is set in the .env file, initialize without arguments
client = KruncherClient()

# Fetch projects
df_projects = client.get_projects(page=0)
print(df_projects)

# Fetch projects as a DataFrame
projects_df = client.get_projects_df_full(page=0)
print(projects_df)

# Fetch analysis details
analysis_id = 'your_analysis_id_here'
analysis_details = client.get_analysis_detail(analysis_id=analysis_id)
print(analysis_details)
```

---

## 📌 Features

- 🔍 **Retrieve projects** from Kruncher API.
- 📊 **Fetch projects as a DataFrame** for easy analysis.
- 📈 **Get analysis details** using an `analysis_id`.
- 🔒 **Secure API key storage** via `.env` file or environment variables.

---

## ❓ Need Help?

For any issues, feel free to reach out:

- 📧 **Support**: [info@kruncher.ai](mailto:info@kruncher.ai)
- 🛠 **GitHub Issues**: [Report Issues](https://github.com/your-repo/issues)

Enjoy using `kruncher-client`! 🚀

