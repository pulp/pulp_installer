describe directory('/etc/') do
  its('owner') { should eq 'root' }
end

['pulp-resource-manager', 'pulp-worker@1', 'pulp-worker@2'].each do |pservice|
  describe service(pservice) do
    it { should be_running }
    it { should be_enabled }
  end
end
