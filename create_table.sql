-- auto-generated definition
create table events
(
    id         int unsigned auto_increment
        primary key,
    created_at datetime      default CURRENT_TIMESTAMP not null,
    user       varchar(255)  default ''                not null,
    type       varchar(255)  default ''                not null,
    extra      varchar(4096) default ''                not null,
    client_ip  varchar(255)  default ''                not null
)
    collate = utf8mb4_estonian_ci;

create index events_type_created_at_user_index
    on events (type, created_at, user);

create index events_user_index
    on events (user);