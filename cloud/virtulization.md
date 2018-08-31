# 虚拟化
Hypervisor是用来控制虚拟机的程序。根据 Hypervisor的实现方式和所处的位置，虚拟化又分为两种：1型虚拟化和2型虚拟化。
- 1型虚拟化，Hypervisor 直接安装在物理机上，多个虚拟机在 Hypervisor 上运行。Hypervisor 实现方式一般是一个特殊定制的 Linux 系统。Xen 和 VMWare 的 ESXi 都属于这个类型；
- 2型虚拟化，物理机上首先安装常规的操作系统，比如 Redhat、Ubuntu 和 Windows。Hypervisor 作为 OS 上的一个程序模块运行，并对管理虚拟机进行管理。KVM、VirtualBox 和 VMWare Workstation 都属于这个类型。

比较：
- 1型虚拟化一般对硬件虚拟化功能进行了特别优化，性能上比2型要高；
- 2型虚拟化因为基于普通的操作系统，会比较灵活，比如支持虚拟机嵌套。嵌套意味着可以在KVM虚拟机中再运行KVM。

## KVM
KVM 全称是 Kernel-Based Virtual Machine。也就是说 KVM 是基于 Linux 内核实现的。KVM有一个内核模块叫 kvm.ko，只用于管理虚拟 CPU 和内存。那 IO 的虚拟化，比如存储和网络设备由谁实现呢？作为一个 Hypervisor，KVM 本身只关注虚拟机调度和内存管理这两个方面。IO 外设的任务交给 Linux 内核和 Qemu。

### Libvirt
Libvirt 除了能管理 KVM 这种 Hypervisor，还能管理 Xen，VirtualBox 等。OpenStack 底层也使用 Libvirt。Libvirt 包含 3 个东西：后台 daemon 程序 libvirtd、API 库和命令行工具 virsh
libvirtd是服务程序，接收和处理 API 请求；
API 库使得其他人可以开发基于 Libvirt 的高级工具，比如 virt-manager，这是个图形化的 KVM 管理工具，后面我们也会介绍；

### CPU虚拟化
KVM的虚拟化由CPU硬件支持，一个 KVM 虚机在宿主机中其实是一个 qemu-kvm 进程，与其他 Linux 进程一样被调度，虚机中的每一个虚拟 vCPU 则对应 qemu-kvm 进程中的一个线程。（虚机的 vCPU 总数可以超过物理 CPU 数量，这个叫 CPU overcommit（超配））

### 内存虚拟化
KVM 需要实现 VA（虚拟内存） -> PA（物理内存） -> MA（机器内存）之间的地址转换。虚机 OS 控制虚拟地址到客户内存物理地址的映射 （VA -> PA），但是虚机 OS 不能直接访问实际机器内存，因此 KVM 需要负责映射客户物理内存到实际机器内存 （PA -> MA）。

### 存储虚拟化
KVM 的存储虚拟化是通过存储池（Storage Pool）和卷（Volume）来管理的。Storage Pool 是宿主机上可以看到的一片存储空间，可以是多种类型，Volume 是在 Storage Pool 中划分出的一块空间，宿主机将 Volume 分配给虚拟机，Volume 在虚拟机中看到的就是一块硬盘。 KVM 所有可以使用的 Storage Pool 都定义在宿主机的/etc/libvirt/storage 目录下，每个 Pool一个xml 文件，默认有一个 default.xml。

- StoragePool类型：
    - 目录类型（/var/lib/libvirt/images/ ），Volume以文件方式管理，使用文件做 Volume 有很多优点：存储方便、移植性好、可复制、可远程访问（NFS）。KVM支持的几种Volume如下：
        - raw 是默认格式，即原始磁盘镜像格式，移植性好，性能好，但大小固定，不能节省磁盘空间。
        - qcow2 是推荐使用的格式，cow 表示 copy on write，更小的占用空间，能够节省磁盘空间，支持 AES 加密，支持 zlib 压缩，支持多快照，功能很多。
        - vmdk 是 VMWare 的虚拟磁盘格式，也就是说 VMWare 虚机可以直接在 KVM上 运行。
    - LVM的Storage Pool，VG为Storage Pool，LV为作为虚拟机磁盘，LV由于没有磁盘的 MBR 引导记录，不能作为虚拟机的启动盘，只能作为数据盘使用。
        - LV 的优点是有较好的性能；
        - 不足的地方是管理和移动性方面不如镜像文件，而且不能通过网络远程使用。
        
> PV、VG、LV
- PV(physical volume)：物理卷在逻辑卷管理系统最底层，可为整个物理硬盘或实际物理硬盘上的分区;
- VG(volume group)：卷组建立在物理卷上，一卷组中至少要包括一物理卷，卷组建立后可动态的添加卷到卷组中，一个逻辑卷管理系统工程中可有多个卷组;
- LV(logical volume)：逻辑卷建立在卷组基础上，卷组中未分配空间可用于建立新的逻辑卷，逻辑卷建立后可以动态扩展和缩小空间。

### 网络虚拟化
- Linux Bridge 是 Linux 上用来做 TCP/IP 二层协议交换的设备，其功能大家可以简单的理解为是一个二层交换机或者 Hub。多个网络设备可以连接到同一个 Linux Bridge，当某个设备收到数据包时，Linux Bridge 会将数据转发给其他设备。
- VLAN





