version_info    = (0, 1, 0, 'final', 0)
version_info_js = (0, 1, 0, 'final', 0)

_specifier_ = {'alpha': 'a', 'beta': 'b', 'candidate': 'rc', 'final': ''}

__version__ = '%s.%s.%s%s'%(version_info[0], version_info[1], version_info[2],
  '' if version_info[3]=='final' else _specifier_[version_info[3]]+str(version_info[4]))


__version_js__ = '%s.%s.%s%s'%(version_info_js[0], version_info_js[1], version_info_js[2],
  '' if version_info[3]=='final' else '-%s.%s' % (version_info_js[3], str(version_info_js[4])))
