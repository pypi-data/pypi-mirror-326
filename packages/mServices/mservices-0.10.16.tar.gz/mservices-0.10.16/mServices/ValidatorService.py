import re
from datetime import datetime

class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__("Validation failed.")

class ValidatorService:
    @staticmethod
    def validate(request, rules, custom_messages=None):
        errors = {}
        custom_messages = custom_messages or {}

        for field, rule_set in rules.items():
            value = request.get(field)
            rule_list = rule_set.split('|')

            for rule in rule_list:
                if rule == "required" and not value:
                    ValidatorService.add_error(
                        errors, field, "required", custom_messages, _attribute=field
                    )

                elif rule.startswith("min:"):
                    min_length = int(rule.split(":")[1])
                    if value and len(value) < min_length:
                        ValidatorService.add_error(
                            errors, field, "min", custom_messages, 
                            _attribute=field, min=min_length
                        )

                elif rule.startswith("max:"):
                    max_length = int(rule.split(":")[1])
                    if value and len(value) > max_length:
                        ValidatorService.add_error(
                            errors, field, "max", custom_messages, 
                            _attribute=field, max=max_length
                        )

                elif rule == "email":
                    if value and not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                        ValidatorService.add_error(
                            errors, field, "email", custom_messages, _attribute=field
                        )

                elif rule.startswith("date_format:"):
                    date_format = rule.split(":")[1]
                    try:
                        datetime.strptime(value, date_format)
                    except (ValueError, TypeError):
                        ValidatorService.add_error(
                            errors, field, "date_format", custom_messages, 
                            _attribute=field, format=date_format
                        )

        if errors:
            raise ValidationError(errors)

        return True

    @staticmethod
    def add_error(errors, field, error_type, custom_messages, **tokens):
        if field not in errors:
            errors[field] = []

        errors[field].append({
            "error_type": error_type,
            "tokens": tokens
        })
