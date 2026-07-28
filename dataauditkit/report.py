from .profile import ProfileReport
from .config import ReportConfig


def report(df, target=None, output=False):
    config = ReportConfig()
    if not output:
        config.generate_plots = False

    profile = ProfileReport(df, target=target, config=config)
    results = profile.compute()

    if output:
        config.generate_plots = True
        profile.to_html()

    return profile.to_dict()
