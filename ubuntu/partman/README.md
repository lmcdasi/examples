Snapshot of a sample partman disk parition
having BTRFS as one of the file system used.

### Partitioning
d-i partman-auto/method string regular
d-i partman-lvm/device_remove_lvm boolean true
d-i partman-md/device_remove_md boolean true
d-i partman-lvm/confirm boolean true
d-i partman-auto/expert_recipe string gpt-boot-root :     \
          1     1   1 free                                \
                  $bios_boot{ }                           \
                  method{ biosgrub }                      \
          .                                               \
          200 200 200 fat32                               \
                  label{ EFI }                            \
                  $primary{ }                             \
                  method{ efi } format{ }                 \
          .                                               \
          512 512 512 ext3                                \
                  $primary{ } $bootable{ }                \
                  method{ format } format{ }              \
                  use_filesystem{ } filesystem{ ext3 }    \
                  mountpoint{ /boot }                     \
          .                                               \
          1000 512 5000 ext4                              \
                  $primary{ }                             \
                  method{ format } format{ }              \
                  use_filesystem{ } filesystem{ ext4 }    \
                  mountpoint{ /usr/local/k3/log }         \
          .                                               \
          1000 512 5000 ext4                              \
                  $primary{ }                             \
                  method{ format } format{ }              \
                  use_filesystem{ } filesystem{ ext4 }    \
                  mountpoint{ /var/log }                  \
          .                                               \
          5000 512 -1 btrfs                               \
                  $primary{ }                             \
                  method{ format } format{ }              \
                  use_filesystem{ } filesystem{ btrfs }   \
                  mountpoint{ / }                         \
          .

# This makes partman automatically partition without confirmation.
d-i partman-partitioning/confirm_write_new_label boolean true
d-i partman/choose_partition select finish
d-i partman/confirm boolean true
d-i partman/confirm_nooverwrite boolean true
