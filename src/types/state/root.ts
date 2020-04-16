import { ConfigInfo } from "../config-info";

export interface BackendConfig {
  SITE_NAME:                      string;
  SITE_LOGO_TEXT:                 string;
  SITE_TITLE_TEXT:                string;
  SITE_URL:                       string;
  SITE_CONTACT_EMAIL:             string;
  ABOUT_PAGE_ENABLE:              boolean;
  ABOUT_CUSTOM_HTML:              string;
  SIGNUP_LICENSE_HTML:            string;
  FOOTER_EXTRA_HTML:              string;
  USER_SECURE_AUTH_FRONTEND_SALT: string;
  WIKI_ENABLE:                    boolean;
  SEARCH_ENABLE:                  boolean;
  USER_NICKNAME_MIN:              number;
  USER_NICKNAME_MAX:              number;
  USER_NICKNAME_CN_FOR_REG_MIN:   number;
  USER_NICKNAME_FOR_REG_MIN:      number;
  USER_NICKNAME_FOR_REG_MAX:      number;
  USER_PASSWORD_MIN:              number;
  USER_PASSWORD_MAX:              number;
  TOPIC_TITLE_LENGTH_MIN:         number;
  TOPIC_TITLE_LENGTH_MAX:         number;
  TOPIC_CONTENT_LENGTH_MAX:       number;
  EMAIL_ACTIVATION_ENABLE:        boolean;
  UPLOAD_ENABLE:                  boolean;
  UPLOAD_BACKEND:                 string;
  UPLOAD_STATIC_HOST:             string;
  UPLOAD_QINIU_DEADLINE_OFFSET:   number;
  UPLOAD_QINIU_IMAGE_STYLE_TOPIC: string;
}

export interface PostState {
  DEL:    number;
  APPLY:  number;
  CLOSE:  number;
  NORMAL: number;
}

export interface PostTypes {
  NONE:    number;
  USER:    number;
  BOARD:   number;
  TOPIC:   number;
  WIKI:    number;
  COMMENT: number;
  MENTION: number;
  UPLOAD:  number;
}

export interface PostVisible {
  HIDE:             number;
  PRIVATE:          number;
  NOT_IN_LIST:      number;
  NORMAL:           number;
  CONTENT_IF_LOGIN: number;
  USER_ONLY:        number;
  ADMIN_ONLY:       number;
}

export interface UserGroup {
  BAN:       number;
  INACTIVE:  number;
  NORMAL:    number;
  SUPERUSER: number;
  ADMIN:     number;
}

export interface Extra {
  midnight_time: number;
}

export interface NotifType {
  BE_COMMENTED:         number;
  BE_REPLIED:           number;
  BE_FOLLOWED:          number;
  BE_MENTIONED:         number;
  BE_BOOKMARKED:        number;
  BE_LIKED:             number;
  BE_SENT_PM:           number;
  MANAGE_INFO_ABOUT_ME: number;
  SYSTEM_MSG:           number;
}

export interface BackendConfigMisc {
  POST_TYPES:           PostTypes,
  POST_TYPES_TXT:       { [key: string]: string },
  POST_STATE:           PostState,
  POST_STATE_TXT:       { [key: string]: string };
  POST_VISIBLE:         PostVisible;
  POST_VISIBLE_TXT:     { [key: string]: string };
  MANAGE_OPERATION:     { [key: string]: number };
  MANAGE_OPERATION_TXT: { [key: string]: string };
  USER_GROUP:           UserGroup;
  USER_GROUP_TXT:       { [key: string]: string };
  USER_GROUP_TO_ROLE:   { [key: string]: string };
  NOTIF_TYPE:           NotifType;
  BACKEND_CONFIG:       BackendConfig;
  retcode:              { [key: string]: number };
  retinfo_cn:           any;
  extra:                Extra;
}

export interface RootState {
  misc: BackendConfigMisc,
  loading: number,
  msgs: Array<any>,
  messageId: number,
  online: number,
  _initing: boolean,

  config: ConfigInfo
}
