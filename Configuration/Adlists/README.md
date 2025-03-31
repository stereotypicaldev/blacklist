# Pi-hole Adlist Configuration

This directory contains a collection of custom adlist configurations for Pi-hole. 

These lists can be used to block advertisements, trackers, and other unwanted content from various sources on your network. Pi-hole is a network-wide ad blocker that acts as a DNS sinkhole.

## Overview

This directory contains a set of curated adlists that can be added to your Pi-hole instance to enhance the blocking capabilities. Each adlist is carefully selected based on specific categories such as:

- **Ads**: Common advertising domains.
- **Trackers**: Domains related to online tracking and analytics.
- **Malware**: Known domains associated with malicious activity.
- **Misc**:
    - **Social Media**: Block domains that serve social media scripts or trackers.

The lists are in a format that Pi-hole can use directly, and they can be added through the Pi-hole web interface or by directly modifying the Pi-hole configuration files.

## How to Use

### Method 1: Pi-hole Dashboard

There are two ways to add these adlists to your Pi-hole configuration:

- Method 1: Pi-hole Web Interface

- Open your Pi-hole web interface.

- Navigate to Group Management > Adlists.

- Add each URL from the adlists in this repository.

- Save the changes and update your Pi-hole setup by clicking "Update Gravity" to apply the new adlists.

### Method 2: Command Line

You can manually add the adlists by modifying the adlists.list file:

SSH into your Pi-hole server.

Open the adlist file:

```bash
sudo nano /etc/pihole/adlists.list
```

Copy and paste the URLs from this repository into the adlists.list file.

Save and exit the editor.

Update Pi-hole gravity:

```bash
pihole -g
```