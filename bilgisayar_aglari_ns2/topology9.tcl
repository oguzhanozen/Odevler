# NS2 9 düğümlü topoloji - UDP + TCP trafik
set ns [new Simulator]

set nf [open topology9.nam w]
set tf [open topology9.tr w]
$ns namtrace-all $nf
$ns trace-all $tf

# Düğümler
for {set i 0} {$i < 9} {incr i} {
    set n($i) [$ns node]
}

# Bağlantılar (yatay ve dikey)
$ns duplex-link $n(0) $n(1) 1Mb 10ms DropTail
$ns duplex-link $n(1) $n(2) 1Mb 10ms DropTail

$ns duplex-link $n(3) $n(4) 1Mb 10ms DropTail
$ns duplex-link $n(4) $n(5) 1Mb 10ms DropTail

$ns duplex-link $n(6) $n(7) 1Mb 10ms DropTail
$ns duplex-link $n(7) $n(8) 1Mb 10ms DropTail

$ns duplex-link $n(0) $n(3) 1Mb 10ms DropTail
$ns duplex-link $n(3) $n(6) 1Mb 10ms DropTail

$ns duplex-link $n(1) $n(4) 1Mb 10ms DropTail
$ns duplex-link $n(4) $n(7) 1Mb 10ms DropTail

$ns duplex-link $n(2) $n(5) 1Mb 10ms DropTail
$ns duplex-link $n(5) $n(8) 1Mb 10ms DropTail

# UDP → CBR: n0 → n8
set udp0 [new Agent/UDP]
$ns attach-agent $n(0) $udp0
set null0 [new Agent/Null]
$ns attach-agent $n(8) $null0
$ns connect $udp0 $null0

set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 512
$cbr0 set interval_ 0.01
$cbr0 attach-agent $udp0

# TCP → FTP: n2 → n6
set tcp1 [new Agent/TCP]
$ns attach-agent $n(2) $tcp1
set sink1 [new Agent/TCPSink]
$ns attach-agent $n(6) $sink1
$ns connect $tcp1 $sink1

set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1

# Trafik başlatma ve durdurma
$ns at 1.0 "$cbr0 start"
$ns at 1.2 "$ftp1 start"
$ns at 4.8 "$cbr0 stop"
$ns at 5.0 "finish"

# Bitirme fonksiyonu
proc finish {} {
    global ns nf tf
    $ns flush-trace
    close $nf
    close $tf
    exec nam topology9.nam &
    exit 0
}

$ns run
