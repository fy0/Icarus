# for peewee 2.9.1

import playhouse.shortcuts


def apply_to_dict_patch():
    old_model_to_dict = playhouse.shortcuts.model_to_dict

    # noinspection PyProtectedMember
    def my_model_to_dict(model, recurse=True, backrefs=False, only=None,
                         exclude=None, seen=None, extra_attrs=None,
                         fields_from_query=None, max_depth=None):

        if hasattr(model, '_meta') and hasattr(model._meta, 'to_dict'):
            if 'exclude' in model._meta.to_dict:
                new_exclude = []
                tmodel = type(model)
                # it's impossible to get field object before class defined
                # so I must convert them
                for i in model._meta.to_dict['exclude']:
                    new_exclude.append(getattr(tmodel, i))
                if exclude:
                    exclude.extend(new_exclude)
                else:
                    exclude = new_exclude

            if 'extra_attrs' in model._meta.to_dict:
                if extra_attrs:
                    extra_attrs.extend(model._meta.to_dict['extra_attrs'])
                else:
                    extra_attrs = model._meta.to_dict['extra_attrs']

        return old_model_to_dict(model, recurse=recurse, backrefs=backrefs, only=only, exclude=exclude,
                                 extra_attrs=extra_attrs, fields_from_query=fields_from_query, seen=seen,
                                 max_depth=max_depth)

    playhouse.shortcuts.model_to_dict = my_model_to_dict
