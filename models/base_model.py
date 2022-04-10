class BaseModel:

    def __init__(self, primary_key,  field_names, field_values):
        self.primary_key = primary_key
        for name, value in zip(field_names, field_values):
            setattr(self, name, value)

    def __str__(self):
        instance_attrs_repr = ' '.join(f'{attr_name}: {attr_value}' for attr_name, attr_value in self.__dict__.items())
        return f'{self.__class__.__name__}. {instance_attrs_repr}'

    __repr__ = __str__

    def get_diff(self, obj):
        """
        Method that compares two instances of models

        :param obj: instance of a model
        :return: string that contains differences between model objects
        """
        diff_msg = ''
        for attr in self.__dict__:
            left_instance_attr = getattr(self, attr)
            right_instance_attr = getattr(obj, attr)
            if self.primary_key != obj.primary_key:
                return f'Value for row {self.__class__.__name__.lower()} for does not match with expected.\n\t\t' \
                       f'Expected: {self.primary_key}.' \
                       f'Actual: {obj.primary_key}.\n'
            elif left_instance_attr != right_instance_attr:
                if isinstance(left_instance_attr, BaseModel):
                    diff_msg += left_instance_attr.get_diff(right_instance_attr)
                else:
                    diff_msg += f'Value for row {attr} does not match with expected.\n\t\t' \
                                f'Expected: {getattr(self, attr)}. Actual: {getattr(obj, attr)}\n'
        return diff_msg

    def __eq__(self, obj):
        return not self.get_diff(obj)
