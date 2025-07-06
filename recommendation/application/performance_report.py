def evaluate_user_performance(user, usage, package):
    def percent(used, limit):
        return round((used / limit) * 100, 2) if limit > 0 else 0

    internet_percent = percent(usage.internet_used, package.internet_limit)
    call_percent = percent(usage.call_used, package.call_limit)
    sms_percent = percent(usage.sms_used, package.sms_limit)

    average_usage = round((internet_percent + call_percent + sms_percent) / 3, 2)

    if average_usage < 30:
        status = "Low Usage"
    elif average_usage < 80:
        status = "Moderate Usage"
    elif average_usage < 95:
        status = "Good Usage"
    else:
        status = "Excellent"
        

    return {
        "user": user.username,
        "month": usage.month.strftime("%Y-%m"),
        "package": {
            "name": package.package_name,
            "limits": {
                "internet": package.internet_limit,
                "calls": package.call_limit,
                "sms": package.sms_limit
            }
        },
        "usage": {
            "internet_used": usage.internet_used,
            "calls_used": usage.call_used,
            "sms_used": usage.sms_used
        },
        "percentages": {
            "internet": internet_percent,
            "calls": call_percent,
            "sms": sms_percent
        },
        "summary": {
            "average_usage_percent": average_usage,
            "status": status,
        }
    }
