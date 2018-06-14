describe directory('/etc/') do
  its('owner') { should eq 'root' }
end
