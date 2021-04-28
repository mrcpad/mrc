name:   mrc
%define _prefix    /usr/local/bin
Version:        2.30
Release:        3
Summary:        mrc
License:        trywangdao@gmail.com
Group:          github
Prefix: %{_prefix}
%description
%prep
%files
%defattr(0755,root,root,-)
%{_prefix}
#/usr/local/bin/  
%doc
%pre
%post
echo %{_prefix} >> $HOME/.bashrc
%changelog
