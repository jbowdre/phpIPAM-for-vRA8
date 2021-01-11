FROM photon:3.0-20200609

ADD target/python /ipam/python

RUN tdnf install -y python3-pip.noarch python3-devel gcc glibc-devel binutils linux-api-headers shadow && \
    pip3 install --upgrade pip setuptools && \
    pip3 install certifi && \
    tdnf clean all && \
    rm -fr /var/cache/tdnf/*

RUN pip3 install -r /ipam/python/allocate_ip/requirements.txt --target=/ipam/python/allocate_ip
RUN pip3 install -r /ipam/python/deallocate_ip/requirements.txt --target=/ipam/python/deallocate_ip
RUN pip3 install -r /ipam/python/get_ip_ranges/requirements.txt --target=/ipam/python/get_ip_ranges
RUN pip3 install -r /ipam/python/validate_endpoint/requirements.txt --target=/ipam/python/validate_endpoint
RUN if [ "@provider.supportsUpdateRecord@" = "true" ] ; then pip3 install -r /ipam/python/update_record/requirements.txt --target=/ipam/python/update_record ; fi
RUN if [ "@provider.supportsOnDemandNetworks@" = "true" ] ; then pip3 install -r /ipam/python/get_ip_blocks/requirements.txt --target=/ipam/python/get_ip_blocks ; fi
RUN if [ "@provider.supportsOnDemandNetworks@" = "true" ] ; then pip3 install -r /ipam/python/allocate_ip_range/requirements.txt --target=/ipam/python/allocate_ip_range ; fi
RUN if [ "@provider.supportsOnDemandNetworks@" = "true" ] ; then pip3 install -r /ipam/python/deallocate_ip_range/requirements.txt --target=/ipam/python/deallocate_ip_range ; fi

RUN useradd -ms /bin/bash -u @user.id@ -U @user.name@

CMD yes | cp -rf -R /ipam/python /ipam/result && \
    echo Collecting-dependencies-complete
