def calculate_usage_percentages(usage, package):
    def percent(used, limit):
        return round((used / limit) * 100, 2) if limit > 0 else 0

    return {
        "internet_percent": percent(usage.internet_used, package.internet_limit),
        "call_percent": percent(usage.call_used, package.call_limit),
        "sms_percent": percent(usage.sms_used, package.sms_limit),
        "package_name": package.package_name,
        "month": usage.month.strftime("%Y-%m")
    }