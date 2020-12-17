FROM mltooling/build-environment:0.6.1

COPY extended-entrypoint.sh /extended-entrypoint.sh

RUN chmod +x /extended-entrypoint.sh

ENTRYPOINT ["/tini", "-g", "--", "/extended-entrypoint.sh"]