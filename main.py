from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from urllib.parse import urlparse
import re

Window.clearcolor = (0.02, 0.03, 0.04, 1)


class PhishGuard(App):

    def build(self):

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=12
        )

        title = Label(
            text="PHISHGUARD",
            font_size=28,
            bold=True,
            color=(0, 1, 0.45, 1),
            size_hint_y=None,
            height=60
        )

        subtitle = Label(
            text="CYBERSECURITY • URL THREAT ANALYZER",
            font_size=12,
            color=(0.6, 0.65, 0.7, 1),
            size_hint_y=None,
            height=35
        )

        self.url = TextInput(
            hint_text="Enter website URL",
            multiline=False,
            size_hint_y=None,
            height=55
        )

        scan = Button(
            text="SCAN URL",
            size_hint_y=None,
            height=55,
            background_color=(0, 0.9, 0.4, 1)
        )

        scan.bind(on_press=self.scan_url)

        self.result = Label(
            text="WAITING FOR SCAN",
            font_size=18,
            bold=True
        )

        self.details = Label(
            text="",
            font_size=14,
            halign="left",
            valign="top"
        )

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(self.url)
        layout.add_widget(scan)
        layout.add_widget(self.result)
        layout.add_widget(self.details)

        return layout

    def scan_url(self, instance):

        url = self.url.text.strip()

        if not url:
            self.result.text = "ENTER A URL"
            self.details.text = ""
            return

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        score = 0
        reasons = []

        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        if "@" in url:
            score += 3
            reasons.append("• @ symbol detected")

        if len(url) >= 54:
            score += 1
            reasons.append("• URL is unusually long")

        if parsed.scheme != "https":
            score += 1
            reasons.append("• HTTPS is missing")

        if "-" in domain:
            score += 1
            reasons.append("• Hyphen found in domain")

        if re.match(r"^(?:\d{1,3}\.){3}\d{1,3}$", domain):
            score += 3
            reasons.append("• IP address used")

        suspicious = [
            "login",
            "verify",
            "secure",
            "account",
            "update",
            "banking"
        ]

        for word in suspicious:
            if word in url.lower():
                score += 1
                reasons.append(
                    "• Suspicious word: " + word
                )

        if score >= 5:
            level = "HIGH"
            self.result.text = "DANGER: PHISHING URL"
            self.result.color = (1, 0.1, 0.2, 1)

        elif score >= 2:
            level = "MEDIUM"
            self.result.text = "WARNING: SUSPICIOUS URL"
            self.result.color = (1, 0.7, 0, 1)

        else:
            level = "LOW"
            self.result.text = "SAFE: NO MAJOR THREAT"
            self.result.color = (0, 1, 0.45, 1)

        self.details.text = (
            "Risk Level: " + level +
            "\nRisk Score: " + str(score) +
            "\n\n" +
            ("\n".join(reasons)
             if reasons
             else "• No major threat indicators detected.")
        )


PhishGuard().run()