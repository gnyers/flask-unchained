from py_meta_utils import McsArgs, MetaOption, deep_getattr
from sqlalchemy.orm import RelationshipProperty
from sqlalchemy_unchained import ModelMetaOptionsFactory as BaseMetaOptionsFactory
from typing import *


class RelationshipsMetaOption(MetaOption):
    def __init__(self):
        super().__init__('relationships', inherit=True)

    def get_value(self, meta, base_model_meta, mcs_args: McsArgs):
        """overridden to merge with inherited value"""
        if mcs_args.model_meta.abstract:
            return None
        value = getattr(base_model_meta, self.name, {}) or {}
        value.update(getattr(meta, self.name, {}))
        return value

    def contribute_to_class(self, mcs_args: McsArgs, relationships):
        if mcs_args.model_meta.abstract:
            return

        discovered_relationships = {}

        def discover_relationships(d):
            for k, v in d.items():
                if isinstance(v, RelationshipProperty):
                    discovered_relationships[v.argument] = k
                    if v.backref and mcs_args.model_meta.lazy_mapped:
                        raise Exception(
                            f'Discovered a lazy-mapped backref `{k}` on '
                            f'`{mcs_args.model_repr}`. Currently this '
                            'is unsupported; please use `db.relationship` with '
                            'the `back_populates` kwarg on both sides instead.')

        for base in mcs_args.bases:
            discover_relationships(vars(base))
        discover_relationships(mcs_args.clsdict)

        relationships.update(discovered_relationships)


class MaterializedViewForMetaOption(MetaOption):
    def __init__(self):
        super().__init__(name='mv_for', default=None, inherit=True)

    def get_value(self, meta, base_model_meta, mcs_args: McsArgs):
        return super().get_value(meta, base_model_meta, mcs_args) or []


class ModelMetaOptionsFactory(BaseMetaOptionsFactory):
    def _get_meta_options(self) -> List[MetaOption]:
        """"
        Define fields allowed in the Meta class on end-user models, and the
        behavior of each.

        Custom ModelMetaOptions classes should override this method to customize
        the options supported on class Meta of end-user models.
        """
        return super()._get_meta_options() + [RelationshipsMetaOption(),
                                              MaterializedViewForMetaOption()]

    @property
    def _is_base_polymorphic_model(self):
        if not self.polymorphic:
            return False
        base_meta = deep_getattr({}, self._mcs_args.bases, '_meta')
        return base_meta.abstract

    @property
    def _model_repr(self):
        return self._mcs_args.model_repr

    def __repr__(self):
        return '<{cls} model={model!r} model_meta_options={attrs!r}>'.format(
            cls=self.__class__.__name__,
            model=self._model_repr,
            attrs={option.name: getattr(self, option.name, None)
                   for option in self._get_meta_options()})