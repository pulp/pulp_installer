describe directory('/etc/') do
  its('owner') { should eq 'root' }
end

['pulpcore-resource-manager', 'pulpcore-worker@1', 'pulpcore-worker@2'].each do |pservice|
  describe service(pservice) do
    it { should be_running }
    it { should be_enabled }
  end
end
