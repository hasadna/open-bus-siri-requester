# Pulled April 26, 2021
FROM nginx@sha256:75a55d33ecc73c2a242450a9f1cc858499d468f077ea942867e662c247b5e412
COPY default.conf /etc/nginx/conf.d/
COPY entrypoint.sh /etc/nginx/
ENTRYPOINT ["/etc/nginx/entrypoint.sh"]
