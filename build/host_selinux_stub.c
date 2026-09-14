// Host stub for Android-SELinux specific symbols (external/selinux .../android/android_device.c).
// On a non-Android host (proot aarch64) the SELinux kernel facility is absent, so aapt2's
// resource compiler only needs these symbols to link. They are safe no-ops here.
#include <stddef.h>
#include <sys/types.h>
#include <selinux/android.h>
#include <selinux/label.h>

struct selabel_handle* selinux_android_file_context_handle(void) { return NULL; }
struct selabel_handle* selinux_android_service_context_handle(void) { return NULL; }
struct selabel_handle* selinux_android_hw_service_context_handle(void) { return NULL; }
struct selabel_handle* selinux_android_vendor_service_context_handle(void) { return NULL; }
struct selabel_handle* selinux_android_keystore2_key_context_handle(void) { return NULL; }

void selinux_android_set_sehandle(const struct selabel_handle *hndl) { (void)hndl; }

int selinux_android_setcon(const char *con) { (void)con; return 0; }

int selinux_android_setcontext(uid_t uid, bool isSystemServer,
                               const char *seinfo, const char *name) {
  (void)uid; (void)isSystemServer; (void)seinfo; (void)name; return -1;
}

int selinux_android_context_with_level(const char *context, char **newContext,
                                       uid_t userid, uid_t appid) {
  (void)context; (void)newContext; (void)userid; (void)appid; return -1;
}

int selinux_android_restorecon(const char *file, unsigned int flags) {
  (void)file; (void)flags; return 0;
}

int selinux_android_restorecon_pkgdir(const char *pkgdir, const char *seinfo,
                                      uid_t uid, unsigned int flags) {
  (void)pkgdir; (void)seinfo; (void)uid; (void)flags; return 0;
}

void selinux_android_seapp_context_init(void) {}

int selinux_android_seapp_context_reload(void) { return 0; }
