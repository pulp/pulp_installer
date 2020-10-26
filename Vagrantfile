# -*- mode: ruby -*-
# vi: set ft=ruby :

ROOT_DIR = File.dirname(__FILE__)
VAGRANTFILE_DIR = File.join(ROOT_DIR, 'forklift')
BOX_LOCATIONS = Dir.glob(File.join(ROOT_DIR, 'vagrant', 'boxes.d', '*.yaml'))

require "#{VAGRANTFILE_DIR}/vagrant/lib/forklift"

loader = Forklift::BoxLoader.new("#{VAGRANTFILE_DIR}/vagrant", BOX_LOCATIONS)
loader.load!

distributor = Forklift::BoxDistributor.new(loader.boxes)
distributor.distribute!
