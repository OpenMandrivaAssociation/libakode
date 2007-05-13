%define name libakode
%define version	2.0.2
%define release %mkrel 1
%define major	2
%define lib_name %mklibname akode %major

%define lib_name_orig_kdemultimedia %mklibname kdemultimedia
%define lib_major_kdemultimedia 1
%define lib_name_kdemultimedia %lib_name_orig_kdemultimedia%lib_major_kdemultimedia

%define build_polypaudio 0
%{?_with_polypaudio: %global build_polypaudio 1}


Name: 		%{name}
Summary: 	aKode is the decoding library
Version: 	%{version}
Release: 	%{release}
Group: 		System/Libraries
License: 	LGPL
URL: 		http://www.carewolf.com/akode/
Source:		akode-%version.tar.bz2
Patch0:		akode-2.0.2-flac113-portable.patch
Patch1:		akode-2.0.2-ffmpeg-int64_c.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: autoconf2.5
BuildRequires:	libvorbis-devel liboggflac-devel mad-devel libalsa-devel
BuildRequires:	libsamplerate-devel libltdl-devel jackit-devel
BuildRequires:	speex-devel ffmpeg-devel
%if %build_polypaudio
BuildRequires:  libpolypaudio-devel
%endif

%description
aKode is a simple audio-decoding frame-work that provides a uniform 
interface to decode the most common audio-formats. It also has a 
direct playback option for a number of audio-outputs. 
aKode currently has the following decoder plugins: 
 mpeg: Uses libMAD to decoder all MPEG 1/2 layer I-III audio. 
       GPL licensed and 
       patent issue in the US. 
 mpc:  Decodes musepack aka mpc audio. LGPL licensed. 
 xiph: Decodes FLAC, Ogg/FLAC, Speex and Ogg Vorbis audio. LGPL 
       licensed, patent free. 
 ffmpeg: Experimental decoder using the FFMPEG decoding library. 
       Enables WMA and 
       RealAudio 
       playback. LGPL and possible patent and reengineering issues 
       in the US. 

aKode also has the following audio outputs: 
 oss:  Outputs to the OSS (Open Sound System) of for instance FreeBSD
       and Linux 2.4 
 alsa: Outputs to ALSA of Linux 2.6 (version 0.9 or 1.x required) 
       (dmix is recommended). 
 sun:  Outputs to Sun OS/Solaris audio device . 
 jack: Outputs using Jack audio backend. 
 polyp:Output to the polypaudio server. Recommended for network 
       transparent audio.

%package -n %{lib_name}
Summary: 	Main library for %{name}
Group: 		System/Libraries
Provides: 	%{name} = %{version}-%{release}
Conflicts:	%{lib_name_kdemultimedia}-common < 1:3.5.0-1mdk


%description -n %{lib_name}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{lib_name}-devel
Summary: 	Headers for developing programs that will use %{name}
Group: 		Development/C
Requires: 	%{lib_name} = %{version}-%{release}
Provides: 	akode-devel = %{version}-%{release}
conflicts:	%{lib_name} <= 2.0-5mdk

%description -n %{lib_name}-devel
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%setup -q -n akode-%version
%patch0 -p4
%patch1 -p1

%build
%configure2_5x \
  --with-kscd-cdda \
%if %build_polypaudio
	--with-polypaudio \
%else
	--without-polypaudio \
%endif
  --disable-final \
  --enable-sdl \
  --with-extra-includes=%{_includedir}/speex
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%multiarch_binaries $RPM_BUILD_ROOT/%_bindir/akode-config

%clean 
rm -rf $RPM_BUILD_ROOT

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%files -n %{lib_name}
%defattr(-,root,root)

%_bindir/akodeplay
%_libdir/libakode.so.%{major}*
%_libdir/libakode.la

%_libdir/libakode_alsa_sink.la
%_libdir/libakode_alsa_sink.so
%_libdir/libakode_ffmpeg_decoder.la
%_libdir/libakode_ffmpeg_decoder.so
%_libdir/libakode_jack_sink.la
%_libdir/libakode_jack_sink.so
%_libdir/libakode_mpc_decoder.la
%_libdir/libakode_mpc_decoder.so
%_libdir/libakode_mpeg_decoder.la
%_libdir/libakode_mpeg_decoder.so
%_libdir/libakode_oss_sink.la
%_libdir/libakode_oss_sink.so
%if %build_polypaudio
%_libdir/libakode_polyp_sink.la
%_libdir/libakode_polyp_sink.so
%endif
%_libdir/libakode_src_resampler.la
%_libdir/libakode_src_resampler.so
%_libdir/libakode_xiph_decoder.la
%_libdir/libakode_xiph_decoder.so


%files -n %{lib_name}-devel
%defattr(-,root,root)
%dir %_includedir/akode/
%_includedir/akode/*.h
%_libdir/libakode.so

%_bindir/akode-config
%multiarch %multiarch_bindir/akode-config


